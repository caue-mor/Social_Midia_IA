import uuid
import base64
import logging

from agno.tools import tool

logger = logging.getLogger(__name__)

# Mapping of content types to optimal DALL-E 3 sizes
CONTENT_TYPE_SIZES = {
    "post": "1024x1024",              # Square, works for Instagram/LinkedIn/Facebook
    "story": "1024x1792",             # Vertical 9:16, Instagram/TikTok Stories
    "reel_cover": "1024x1792",        # Vertical 9:16, Reels/Shorts cover
    "youtube_thumbnail": "1792x1024", # Landscape 16:9, YouTube thumbnails
    "carousel_slide": "1024x1024",    # Square, consistent carousel format
}

# Platform-specific size overrides (when platform matters more than content_type)
PLATFORM_SIZE_OVERRIDES = {
    "instagram": {
        "post": "1024x1024",
        "story": "1024x1792",
        "reel_cover": "1024x1792",
        "carousel_slide": "1024x1024",
    },
    "tiktok": {
        "post": "1024x1792",
        "story": "1024x1792",
        "reel_cover": "1024x1792",
    },
    "youtube": {
        "post": "1792x1024",
        "youtube_thumbnail": "1792x1024",
        "reel_cover": "1024x1792",
    },
    "linkedin": {
        "post": "1024x1024",
        "carousel_slide": "1024x1024",
    },
    "twitter": {
        "post": "1792x1024",
    },
    "facebook": {
        "post": "1792x1024",
        "story": "1024x1792",
    },
    "pinterest": {
        "post": "1024x1792",
    },
}

VALID_SIZES = {"1024x1024", "1024x1792", "1792x1024"}
VALID_STYLES = {"vivid", "natural"}


def _resolve_size(content_type: str, platform: str) -> str:
    """Resolve the best DALL-E 3 size for a given content type and platform."""
    platform_lower = platform.lower()
    content_lower = content_type.lower()

    # Check platform-specific override first
    if platform_lower in PLATFORM_SIZE_OVERRIDES:
        platform_sizes = PLATFORM_SIZE_OVERRIDES[platform_lower]
        if content_lower in platform_sizes:
            return platform_sizes[content_lower]

    # Fallback to general content type mapping
    return CONTENT_TYPE_SIZES.get(content_lower, "1024x1024")


def _build_social_media_prompt(content_type: str, description: str, platform: str) -> str:
    """Build an optimized DALL-E 3 prompt for social media content."""
    platform_lower = platform.lower()
    content_lower = content_type.lower()

    # Base style guidance per content type
    style_hints = {
        "post": (
            "Professional social media post image. Clean composition with space "
            "for text overlay. Vibrant colors, high contrast, visually engaging. "
            "No text or letters in the image."
        ),
        "story": (
            "Vertical format image for social media story. Full-bleed composition, "
            "bold visuals, eye-catching. Leave space at top and bottom for UI elements. "
            "No text or letters in the image."
        ),
        "reel_cover": (
            "Vertical cover image for short-form video. Dynamic, attention-grabbing "
            "composition. Bold colors, clear focal point in the center. "
            "No text or letters in the image."
        ),
        "youtube_thumbnail": (
            "YouTube thumbnail style image. High contrast, dramatic lighting, "
            "bold composition. Clear focal point, vibrant saturated colors. "
            "Leave space on the right side for text overlay. "
            "No text or letters in the image."
        ),
        "carousel_slide": (
            "Clean, professional slide image for a carousel post. Consistent style, "
            "balanced composition with space for text overlay. Modern and polished. "
            "No text or letters in the image."
        ),
    }

    # Platform-specific nuances
    platform_hints = {
        "instagram": "Modern, aesthetic, Instagram-worthy visual style.",
        "tiktok": "Bold, trendy, Gen-Z friendly visual style with high energy.",
        "youtube": "Professional, high-quality, cinematic visual style.",
        "linkedin": "Corporate-friendly, professional, clean visual style.",
        "twitter": "Eye-catching, shareable, clean visual style.",
        "facebook": "Engaging, warm, community-friendly visual style.",
        "pinterest": "Aspirational, beautiful, Pinterest-optimized visual style.",
    }

    content_hint = style_hints.get(content_lower, style_hints["post"])
    platform_hint = platform_hints.get(platform_lower, "")

    prompt = (
        f"{content_hint} {platform_hint} "
        f"Description: {description}. "
        "Professional photography quality, studio lighting, 8K detail."
    )

    return prompt


def _upload_to_supabase(image_bytes: bytes, filename: str) -> str:
    """Upload image bytes to Supabase Storage and return the public URL."""
    from app.database.supabase_client import get_supabase

    supabase = get_supabase()
    bucket = "generated-images"

    supabase.storage.from_(bucket).upload(
        path=filename,
        file=image_bytes,
        file_options={"content-type": "image/png", "upsert": "true"},
    )

    public_url = supabase.storage.from_(bucket).get_public_url(filename)
    return public_url


def _generate_image_core(prompt: str, size: str, style: str) -> str:
    """Core image generation logic shared by all image tools.

    Calls DALL-E 3 API, decodes the base64 response, uploads to Supabase Storage,
    and returns the public URL. Falls back to a temporary OpenAI URL if the upload fails.
    """
    from openai import OpenAI
    from app.config import get_settings

    # Validate parameters
    if size not in VALID_SIZES:
        return (
            f"Tamanho invalido: '{size}'. "
            f"Opcoes validas: {', '.join(sorted(VALID_SIZES))}"
        )

    if style not in VALID_STYLES:
        return (
            f"Estilo invalido: '{style}'. "
            f"Opcoes validas: {', '.join(sorted(VALID_STYLES))}"
        )

    try:
        settings = get_settings()
        client = OpenAI(api_key=settings.OPENAI_API_KEY)

        logger.info("Generating image with DALL-E 3: size=%s, style=%s", size, style)

        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size=size,
            style=style,
            quality="hd",
            n=1,
            response_format="b64_json",
        )

        image_data = response.data[0]
        image_b64 = image_data.b64_json
        revised_prompt = image_data.revised_prompt or prompt

        # Decode image bytes
        image_bytes = base64.b64decode(image_b64)

        # Upload to Supabase Storage
        filename = f"{uuid.uuid4().hex}.png"
        try:
            public_url = _upload_to_supabase(image_bytes, filename)
            logger.info("Image uploaded to Supabase: %s", filename)
            return (
                f"Imagem gerada com sucesso!\n\n"
                f"URL: {public_url}\n\n"
                f"Prompt revisado pelo DALL-E: {revised_prompt}"
            )
        except Exception as upload_err:
            logger.warning(
                "Failed to upload to Supabase, returning temporary OpenAI URL: %s",
                upload_err,
            )
            # Fallback: re-generate with URL response to get a temporary link
            fallback_response = client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size=size,
                style=style,
                quality="hd",
                n=1,
                response_format="url",
            )
            temp_url = fallback_response.data[0].url
            return (
                f"Imagem gerada (URL temporaria - upload ao storage falhou)!\n\n"
                f"URL temporaria: {temp_url}\n\n"
                f"Erro no upload: {upload_err}\n\n"
                f"Prompt revisado pelo DALL-E: {revised_prompt}"
            )

    except Exception as e:
        logger.error("Error generating image with DALL-E 3: %s", e)
        return f"Erro ao gerar imagem: {e}"


@tool
def generate_image(prompt: str, size: str = "1024x1024", style: str = "vivid") -> str:
    """Gera uma imagem usando DALL-E 3 da OpenAI e salva no Supabase Storage.

    Args:
        prompt: Descricao detalhada da imagem a ser gerada.
        size: Tamanho da imagem. Opcoes: "1024x1024" (quadrado), "1024x1792" (vertical/story), "1792x1024" (paisagem).
        style: Estilo visual. "vivid" (mais dramatico) ou "natural" (mais realista).

    Returns:
        URL publica da imagem gerada ou mensagem de erro.
    """
    return _generate_image_core(prompt=prompt, size=size, style=style)


@tool
def generate_social_media_image(
    content_type: str,
    description: str,
    platform: str = "instagram",
) -> str:
    """Gera uma imagem otimizada para redes sociais usando DALL-E 3.

    Seleciona automaticamente o tamanho e estilo ideais com base no tipo de conteudo
    e na plataforma alvo.

    Args:
        content_type: Tipo de conteudo. Opcoes: "post", "story", "reel_cover", "youtube_thumbnail", "carousel_slide".
        description: Descricao do que a imagem deve conter (quanto mais detalhada, melhor).
        platform: Plataforma alvo. Opcoes: "instagram", "tiktok", "youtube", "linkedin", "twitter", "facebook", "pinterest".

    Returns:
        URL publica da imagem gerada ou mensagem de erro.
    """
    content_lower = content_type.lower()
    platform_lower = platform.lower()

    valid_content_types = list(CONTENT_TYPE_SIZES.keys())
    if content_lower not in valid_content_types:
        return (
            f"Tipo de conteudo invalido: '{content_type}'. "
            f"Opcoes validas: {', '.join(valid_content_types)}"
        )

    valid_platforms = list(PLATFORM_SIZE_OVERRIDES.keys())
    if platform_lower not in valid_platforms:
        return (
            f"Plataforma invalida: '{platform}'. "
            f"Opcoes validas: {', '.join(valid_platforms)}"
        )

    # Resolve optimal size for this content type + platform combination
    size = _resolve_size(content_lower, platform_lower)

    # Build an optimized prompt for social media
    optimized_prompt = _build_social_media_prompt(content_lower, description, platform_lower)

    # Use "vivid" for social media (more visually striking)
    style = "vivid"

    logger.info(
        "Generating social media image: content_type=%s, platform=%s, size=%s",
        content_lower,
        platform_lower,
        size,
    )

    return _generate_image_core(prompt=optimized_prompt, size=size, style=style)


def get_image_tools() -> list:
    """Returns all image generation tools."""
    return [generate_image, generate_social_media_image]
