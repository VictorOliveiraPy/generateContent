from tools import VIDEOS_DIR, create_transcriptions

for pasta_criador in VIDEOS_DIR.iterdir():
    if pasta_criador.is_dir():
        print(create_transcriptions(pasta_criador.name))
