import os
import time
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("HEYGEN_API_KEY")
HEADERS = {"X-Api-Key": API_KEY, "Content-Type": "application/json"}

VIDEOS_GERADOS_DIR = Path(__file__).parent / "videos_gerados"
VIDEOS_GERADOS_DIR.mkdir(exist_ok=True)


def list_avatars(query: str = "") -> str:
    """Busca avatares disponíveis no HeyGen para escolher qual usar num vídeo. Retorna id, nome e preview de cada um.

    Args:
        query: texto pra filtrar avatares pelo nome (ex: "office", "casual"). Deixe vazio pra listar os primeiros.
    """
    avatares = requests.get("https://api.heygen.com/v2/avatars", headers=HEADERS).json()["data"]["avatars"]
    filtrados = [a for a in avatares if query.lower() in a["avatar_name"].lower()][:20]

    return "\n".join(
        f"{a['avatar_id']} — {a['avatar_name']} ({a['gender']}) — preview: {a['preview_image_url']}"
        for a in filtrados
    )


def generate_avatar_video(script: str, avatar_id: str, voice_id: str) -> str:
    """Gera um vídeo de um avatar do HeyGen falando o texto (engine premium avatar_v), baixa e salva em videos_gerados/. Retorna o caminho local do arquivo.

    Args:
        script: texto que o avatar vai falar
        avatar_id: id do avatar do HeyGen (catálogo deles ou customizado)
        voice_id: id da voz do HeyGen
    """
    resposta = requests.post(
        "https://api.heygen.com/v3/videos",
        headers=HEADERS,
        json={
            "type": "avatar",
            "avatar_id": avatar_id,
            "script": script,
            "voice_id": voice_id,
            "engine": {"type": "avatar_v"},
        },
    )
    if not resposta.ok:
        raise RuntimeError(resposta.text)
    video_id = resposta.json()["data"]["video_id"]

    while True:
        status = requests.get(
            f"https://api.heygen.com/v1/video_status.get?video_id={video_id}", headers=HEADERS
        ).json()["data"]
        if status["status"] == "completed":
            return _baixar(status["video_url"], video_id)
        if status["status"] == "failed":
            raise RuntimeError(status)
        time.sleep(5)


def _baixar(video_url: str, video_id: str) -> str:
    destino = VIDEOS_GERADOS_DIR / f"{video_id}.mp4"
    destino.write_bytes(requests.get(video_url).content)
    return str(destino)
