import httpx
from agno.tools import tool
from app.config import get_settings


@tool
def transcribe_audio(audio_url: str) -> str:
    """Transcreve audio usando OpenAI Whisper API."""
    settings = get_settings()
    if not settings.OPENAI_API_KEY:
        return "OpenAI API nao configurada."

    try:
        # Download do audio
        audio_resp = httpx.get(audio_url, timeout=120)
        audio_resp.raise_for_status()

        # Envia para Whisper
        headers = {"Authorization": f"Bearer {settings.OPENAI_API_KEY}"}
        files = {"file": ("audio.mp3", audio_resp.content, "audio/mpeg")}
        data = {"model": "whisper-1", "language": "pt", "response_format": "verbose_json"}

        resp = httpx.post(
            "https://api.openai.com/v1/audio/transcriptions",
            headers=headers,
            files=files,
            data=data,
            timeout=300,
        )
        resp.raise_for_status()
        result = resp.json()
        return str({
            "text": result.get("text", ""),
            "duration": result.get("duration", 0),
            "segments": [{"start": s["start"], "end": s["end"], "text": s["text"]} for s in result.get("segments", [])[:50]],
        })
    except Exception as e:
        return f"Erro na transcricao: {e}"


@tool
def identify_podcast_clips(transcription: str, min_duration: int = 30, max_duration: int = 90) -> str:
    """Identifica momentos-chave em transcricao de podcast para clips."""
    # Usa o modelo para identificar momentos interessantes
    from openai import OpenAI
    settings = get_settings()
    client = OpenAI(api_key=settings.OPENAI_API_KEY)

    response = client.chat.completions.create(
        model="gpt-4.1-nano",
        messages=[
            {"role": "system", "content": f"Analise esta transcricao e identifique os {3} melhores momentos para clips de {min_duration}-{max_duration} segundos. Retorne JSON com: title, start_time, end_time, description, viral_potential (1-10)."},
            {"role": "user", "content": transcription[:8000]},
        ],
        response_format={"type": "json_object"},
    )
    return response.choices[0].message.content


def get_audio_tools():
    return [transcribe_audio, identify_podcast_clips]
