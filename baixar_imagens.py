from pathlib import Path

import instaloader
from instaloader import Post

LINKS = Path(__file__).parent / "links_imagens.txt"

loader = instaloader.Instaloader(
    filename_pattern="{shortcode}",
    download_videos=False,
    save_metadata=False,
    post_metadata_txt_pattern="",
)

for linha in LINKS.read_text(encoding="utf-8").splitlines():
    partes = linha.split()
    if not partes or partes[0].startswith("#"):
        continue
    link, pasta = partes[0], partes[1] if len(partes) > 1 else "instagram"
    shortcode = link.split("?")[0].rstrip("/").split("/")[-1]
    loader.dirname_pattern = f"referencias/{pasta}"
    loader.download_post(Post.from_shortcode(loader.context, shortcode), target="")
    print(f"baixado: {shortcode} -> referencias/{pasta}")
