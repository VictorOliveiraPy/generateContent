import json
import os
import subprocess
import tempfile
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq()

VIDEOS_DIR = Path(__file__).parent / "videos"
TRANSCRICOES_DIR = Path(__file__).parent / "transcricoes"
TRANSCRICOES_DIR.mkdir(exist_ok=True)


def create_transcriptions(creator: str) -> str:
    """Transcreve todos os vídeos de um criador (pasta em videos/) e salva em transcricoes/<creator>.json.

    Args:
        creator: nome do criador (mesmo nome da pasta em videos/)
    """
    videos = []
    for video in (VIDEOS_DIR / creator).glob("*.mp4"):
        audio_path = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False).name
        subprocess.run(
            ["ffmpeg", "-y", "-i", str(video), "-vn", audio_path],
            check=True, capture_output=True,
        )
        with open(audio_path, "rb") as audio_file:
            resultado = client.audio.transcriptions.create(
                file=(video.name, audio_file),
                model="whisper-large-v3-turbo",
            )
        os.remove(audio_path)
        videos.append({"video": video.name, "transcription": resultado.text})

    (TRANSCRICOES_DIR / f"{creator}.json").write_text(
        json.dumps({creator: videos}, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return f"{len(videos)} vídeo(s) de {creator} transcritos."


def get_transcriptions(creator: str) -> str:
    """Retorna todas as transcrições de vídeos de um criador específico.

    Args:
        creator: nome do criador (mesmo nome da pasta em videos/ usada para baixar os vídeos dele)
    """
    dados = json.loads((TRANSCRICOES_DIR / f"{creator}.json").read_text(encoding="utf-8"))
    videos = dados[creator]

    return "\n\n".join(
        f"Transcript {i}\n{video['transcription']}" for i, video in enumerate(videos, 1)
    )
