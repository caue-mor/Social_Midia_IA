from fastapi import Depends, HTTPException, Security, Request
from fastapi.security import APIKeyHeader, HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from app.config import get_settings, Settings

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)
bearer_scheme = HTTPBearer(auto_error=False)


async def verify_api_key(
    api_key: str = Security(api_key_header),
    settings: Settings = Depends(get_settings),
) -> str:
    if not settings.API_SECRET_KEY:
        return "dev-mode"
    if not api_key or api_key != settings.API_SECRET_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return api_key


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Security(bearer_scheme),
    api_key: str = Security(api_key_header),
    settings: Settings = Depends(get_settings),
) -> dict:
    """Extract user from Supabase JWT or fallback to API key auth."""
    # Try JWT first
    if credentials and credentials.credentials:
        try:
            token = credentials.credentials
            # Supabase JWT uses HS256 with the JWT secret
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
                raise HTTPException(status_code=401, detail="Invalid token: no sub claim")
            return {
                "id": user_id,
                "email": payload.get("email", ""),
                "role": payload.get("role", "authenticated"),
            }
        except JWTError as e:
            raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")

    # Fallback to API key for service-to-service
    if api_key:
        if not settings.API_SECRET_KEY:
            return {"id": "dev-user", "email": "", "role": "service"}
        if api_key == settings.API_SECRET_KEY:
            return {"id": "service-account", "email": "", "role": "service"}

    raise HTTPException(status_code=401, detail="Authentication required")
