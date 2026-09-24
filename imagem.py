import base64
import re
import unicodedata
from datetime import date
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()

IMAGENS_GERADAS_DIR = Path(__file__).parent / "imagens_geradas"
IMAGENS_GERADAS_DIR.mkdir(exist_ok=True)


def _slug(texto: str) -> str:
    sem_acento = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", sem_acento.lower()).strip("-") or "sem-assunto"


def gerar_imagem(prompt: str, nome: str, assunto: str) -> str:
    """Gera uma imagem vertical (formato Reels) a partir de uma descrição e salva em imagens_geradas/<dd-mm-aaaa>/<assunto>/. Retorna o caminho do arquivo.

    Args:
        prompt: descrição detalhada da imagem (cena, estilo, iluminação, enquadramento)
        nome: nome do arquivo sem extensão; use prefixo numérico pra manter a ordem dos slides (ex: 01_abertura)
        assunto: assunto do carrossel (ex: "Evangelho do dia"); todos os slides do mesmo carrossel devem usar exatamente o mesmo valor
    """
    pasta = IMAGENS_GERADAS_DIR / date.today().strftime("%d-%m-%Y") / _slug(assunto)
    pasta.mkdir(parents=True, exist_ok=True)
    resultado = client.images.generate(model="gpt-image-2", prompt=prompt, size="1024x1536")
    destino = pasta / f"{nome}.png"
    destino.write_bytes(base64.b64decode(resultado.data[0].b64_json))
    return str(destino)
