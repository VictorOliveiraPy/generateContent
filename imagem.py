import base64
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()

IMAGENS_GERADAS_DIR = Path(__file__).parent / "imagens_geradas"
IMAGENS_GERADAS_DIR.mkdir(exist_ok=True)


def gerar_imagem(prompt: str, nome: str) -> str:
    """Gera uma imagem vertical (formato Reels) a partir de uma descrição e salva em imagens_geradas/. Retorna o caminho do arquivo.

    Args:
        prompt: descrição detalhada da imagem (cena, estilo, iluminação, enquadramento)
        nome: nome do arquivo sem extensão; use prefixo numérico pra manter a ordem no slideshow (ex: 01_abertura)
    """
    resultado = client.images.generate(model="gpt-image-2", prompt=prompt, size="1024x1536")
    destino = IMAGENS_GERADAS_DIR / f"{nome}.png"
    destino.write_bytes(base64.b64decode(resultado.data[0].b64_json))
    return str(destino)
