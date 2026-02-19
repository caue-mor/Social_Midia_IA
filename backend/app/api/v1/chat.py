import json
import uuid
import logging
from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from fastapi.responses import StreamingResponse
from jose import jwt, JWTError
from app.dependencies import get_current_user
from app.models.schemas import ChatRequest, ChatResponse
from app.agents.team import get_team, get_team_response
from app.config import get_settings
from app.constants import TABLES

logger = logging.getLogger("agentesocial.chat")

router = APIRouter()


@router.post("/", response_model=ChatResponse)
async def send_message(
    request: ChatRequest,
    user: dict = Depends(get_current_user),
):
    result = await get_team_response(
        message=request.message,
        user_id=user["id"],
        conversation_id=request.conversation_id,
        agent_type=request.agent_type,
        context=request.context,
    )
    return result


@router.post("/stream")
async def chat_stream(request: ChatRequest, user: dict = Depends(get_current_user)):
    """SSE streaming endpoint for chat responses."""

    async def event_generator():
        # Send typing event
        yield f"data: {json.dumps({'type': 'typing', 'content': ''})}\n\n"

        try:
            team = get_team()
            user_id = user.get("id", user.get("sub", "anonymous"))
            conversation_id = request.conversation_id or str(uuid.uuid4())

            full_message = request.message
            if request.context:
                context_str = ", ".join(f"{k}: {v}" for k, v in request.context.items())
                full_message = f"[Contexto: user_id={user_id}, {context_str}] {request.message}"
            else:
                full_message = f"[Contexto: user_id={user_id}] {request.message}"

            # Run the team (non-streaming, then stream the response in chunks)
            response = team.run(
                full_message,
                session_id=conversation_id,
                user_id=user_id,
            )
            response_text = response.content if hasattr(response, "content") else str(response)

            # Stream response in chunks for better UX
            words = response_text.split(" ")
            chunk_size = 3  # Send 3 words at a time
            for i in range(0, len(words), chunk_size):
                chunk = " ".join(words[i : i + chunk_size])
                if i > 0:
                    chunk = " " + chunk
                yield f"data: {json.dumps({'type': 'chunk', 'content': chunk})}\n\n"

            # Send done event with metadata
            yield f"data: {json.dumps({'type': 'done', 'conversation_id': conversation_id, 'agent_type': request.agent_type or 'master'})}\n\n"

            # Save conversation (non-blocking)
            try:
                from app.database.supabase_client import get_supabase

                supabase = get_supabase()
                existing = (
                    supabase.table(TABLES["agent_conversations"])
                    .select("messages")
                    .eq("id", conversation_id)
                    .maybe_single()
                    .execute()
                )
                messages = existing.data["messages"] if existing and existing.data else []
                messages.append({"role": "user", "content": request.message})
                messages.append({"role": "assistant", "content": response_text})

                if existing and existing.data:
                    supabase.table(TABLES["agent_conversations"]).update(
                        {"messages": messages, "updated_at": "now()"}
                    ).eq("id", conversation_id).execute()
                else:
                    supabase.table(TABLES["agent_conversations"]).insert(
                        {
                            "id": conversation_id,
                            "user_id": user_id,
                            "agent_type": request.agent_type or "master",
                            "messages": messages,
                        }
                    ).execute()
            except Exception:
                logger.warning(f"Failed to save conversation in stream endpoint: {conversation_id}")

        except Exception as e:
            logger.error(f"SSE stream error for user {user.get('id', 'unknown')}: {e}")
            yield f"data: {json.dumps({'type': 'error', 'content': 'Desculpe, ocorreu um erro. Tente novamente.'})}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


@router.get("/conversations")
async def list_conversations(
    user: dict = Depends(get_current_user),
):
    from app.database.supabase_client import get_supabase
    supabase = get_supabase()
    result = supabase.table(TABLES["agent_conversations"]).select("*").eq("user_id", user["id"]).order("updated_at", desc=True).execute()
    return {"conversations": result.data}


@router.get("/conversations/{conversation_id}/messages")
async def get_conversation(
    conversation_id: str,
    user: dict = Depends(get_current_user),
):
    from app.database.supabase_client import get_supabase
    supabase = get_supabase()
    result = supabase.table(TABLES["agent_conversations"]).select("*").eq("id", conversation_id).eq("user_id", user["id"]).single().execute()
    return result.data


def _authenticate_ws_token(token: str) -> dict | None:
    """Verify a JWT token for WebSocket connections and return user info."""
    settings = get_settings()
    try:
        if settings.SUPABASE_JWT_SECRET:
            payload = jwt.decode(
                token,
                settings.SUPABASE_JWT_SECRET,
                algorithms=["HS256"],
                audience="authenticated",
            )
        else:
            # Dev mode: decode without verification
            payload = jwt.get_unverified_claims(token)
        user_id = payload.get("sub")
        if not user_id:
            return None
        return {
            "id": user_id,
            "email": payload.get("email", ""),
            "role": payload.get("role", "authenticated"),
        }
    except JWTError:
        return None


@router.websocket("/ws")
async def chat_websocket(websocket: WebSocket):
    """WebSocket endpoint for real-time chat with AI agents.

    Authentication: Send a token in the first message or as a query parameter.
    Message format (JSON):
        {
            "token": "jwt-token" (required on first message if not in query params),
            "message": "user message text",
            "conversation_id": "optional-uuid",
            "agent_type": "optional-agent-name",
            "context": { optional context dict }
        }
    Response types:
        {"type": "authenticated", "user_id": "..."}
        {"type": "typing", "status": true/false}
        {"type": "message", "data": { response object }}
        {"type": "error", "message": "error description"}
    """
    await websocket.accept()

    user: dict | None = None

    # Check for token in query params for immediate auth
    query_token = websocket.query_params.get("token")
    if query_token:
        user = _authenticate_ws_token(query_token)
        if user:
            await websocket.send_json({"type": "authenticated", "user_id": user["id"]})
        else:
            await websocket.send_json({"type": "error", "message": "Invalid token"})
            await websocket.close(code=4001, reason="Invalid token")
            return

    try:
        while True:
            raw_data = await websocket.receive_text()

            try:
                message_data = json.loads(raw_data)
            except json.JSONDecodeError:
                await websocket.send_json({"type": "error", "message": "Invalid JSON"})
                continue

            # Authenticate from message token if not yet authenticated
            if user is None:
                msg_token = message_data.get("token")
                if not msg_token:
                    await websocket.send_json({
                        "type": "error",
                        "message": "Authentication required. Send a token field.",
                    })
                    continue
                user = _authenticate_ws_token(msg_token)
                if not user:
                    await websocket.send_json({"type": "error", "message": "Invalid token"})
                    await websocket.close(code=4001, reason="Invalid token")
                    return
                await websocket.send_json({"type": "authenticated", "user_id": user["id"]})

            # Validate message content
            user_message = message_data.get("message", "").strip()
            if not user_message:
                await websocket.send_json({
                    "type": "error",
                    "message": "Empty message. Send a 'message' field with text.",
                })
                continue

            # Send typing indicator ON
            await websocket.send_json({"type": "typing", "status": True})

            # Process through agent team
            try:
                result = await get_team_response(
                    message=user_message,
                    user_id=user["id"],
                    conversation_id=message_data.get("conversation_id"),
                    agent_type=message_data.get("agent_type"),
                    context=message_data.get("context"),
                )
                await websocket.send_json({"type": "message", "data": result})
            except Exception as e:
                logger.error(f"WebSocket agent error for user {user['id']}: {e}")
                await websocket.send_json({
                    "type": "error",
                    "message": "Erro ao processar mensagem. Tente novamente.",
                })
            finally:
                # Send typing indicator OFF
                await websocket.send_json({"type": "typing", "status": False})

    except WebSocketDisconnect:
        logger.info(f"WebSocket disconnected for user {user['id'] if user else 'unauthenticated'}")
    except Exception as e:
        logger.error(f"WebSocket unexpected error: {e}")
        try:
            await websocket.close(code=1011, reason="Internal error")
        except Exception:
            pass
