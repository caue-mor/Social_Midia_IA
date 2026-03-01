"""Validador de contratos com retry automatico para agentes do pipeline.

Garante que agentes retornem JSON estruturado validado contra schemas Pydantic.
Se a validacao falhar, re-prompta o agente com feedback de erro (max 2 retries).
"""

import asyncio
import json
import logging
import re
from typing import Callable, Optional

from pydantic import BaseModel

logger = logging.getLogger("agentesocial.contract_validator")


def extract_json(text: str) -> Optional[str]:
    """Extrai o JSON mais externo de um texto que pode conter markdown."""
    if not text:
        return None

    # Tenta extrair de blocos ```json ... ```
    json_block = re.search(r"```(?:json)?\s*\n?([\s\S]*?)\n?```", text)
    if json_block:
        candidate = json_block.group(1).strip()
        try:
            json.loads(candidate)
            return candidate
        except json.JSONDecodeError:
            pass

    # Procura o objeto/array JSON mais externo
    # Tenta encontrar { ... } ou [ ... ] balanceado
    for start_char, end_char in [("{", "}"), ("[", "]")]:
        start = text.find(start_char)
        if start == -1:
            continue

        depth = 0
        in_string = False
        escape_next = False
        end = start

        for i in range(start, len(text)):
            ch = text[i]
            if escape_next:
                escape_next = False
                continue
            if ch == "\\":
                escape_next = True
                continue
            if ch == '"':
                in_string = not in_string
                continue
            if in_string:
                continue
            if ch == start_char:
                depth += 1
            elif ch == end_char:
                depth -= 1
                if depth == 0:
                    end = i
                    break

        if depth == 0:
            candidate = text[start : end + 1]
            try:
                json.loads(candidate)
                return candidate
            except json.JSONDecodeError:
                continue

    return None


async def validate_and_retry(
    agent_creator: Callable,
    prompt: str,
    schema: type[BaseModel],
    user_id: str,
    max_retries: int = 2,
    session_id: Optional[str] = None,
) -> tuple[BaseModel, str]:
    """Executa agente, valida output contra schema Pydantic, com retry em caso de falha.

    Args:
        agent_creator: Funcao que cria uma instancia fresh do agente (ex: create_social_analyst)
        prompt: Prompt completo para o agente
        schema: Classe Pydantic para validar o output
        user_id: ID do usuario para contexto
        max_retries: Numero maximo de retries em caso de falha de validacao
        session_id: Session ID opcional para o agente

    Returns:
        Tupla (modelo_validado, texto_raw) — modelo com defaults se todas retries falharem
    """
    from app.services.token_manager import set_current_user_id, clear_current_user_id

    schema_json = json.dumps(schema.model_json_schema(), ensure_ascii=False, indent=2)
    enriched_prompt = (
        f"{prompt}\n\n"
        f"IMPORTANTE: Retorne APENAS JSON valido seguindo este schema:\n"
        f"```json\n{schema_json}\n```\n"
        f"Nao inclua texto antes ou depois do JSON."
    )

    raw_text = ""
    last_error = ""

    for attempt in range(1 + max_retries):
        try:
            agent = agent_creator()
            set_current_user_id(user_id)

            run_kwargs = {"message": enriched_prompt, "user_id": user_id}
            if session_id:
                run_kwargs["session_id"] = session_id

            response = await asyncio.to_thread(agent.run, **run_kwargs)
            raw_text = response.content if response and response.content else ""

            json_str = extract_json(raw_text)
            if not json_str:
                last_error = "Nenhum JSON encontrado no output"
                logger.warning(
                    "Attempt %d/%d: no JSON found in agent output (len=%d)",
                    attempt + 1, 1 + max_retries, len(raw_text),
                )
                if attempt < max_retries:
                    enriched_prompt = (
                        f"Seu output anterior nao continha JSON valido. {last_error}. "
                        f"Corrija e retorne APENAS JSON valido seguindo o schema fornecido.\n\n"
                        f"Schema:\n```json\n{schema_json}\n```"
                    )
                continue

            model = schema.model_validate_json(json_str)
            logger.info("Contract validated on attempt %d/%d", attempt + 1, 1 + max_retries)
            return model, raw_text

        except Exception as e:
            last_error = str(e)
            logger.warning(
                "Attempt %d/%d validation failed: %s",
                attempt + 1, 1 + max_retries, last_error,
            )
            if attempt < max_retries:
                enriched_prompt = (
                    f"Seu output nao validou contra o schema. Erro: {last_error}. "
                    f"Corrija e retorne APENAS JSON valido seguindo o schema:\n\n"
                    f"```json\n{schema_json}\n```"
                )
        finally:
            clear_current_user_id()

    # Fallback: retorna modelo com defaults
    logger.error("All %d attempts failed for schema %s. Using defaults.", 1 + max_retries, schema.__name__)
    fallback = schema()
    fallback._raw_text = raw_text
    return fallback, raw_text
