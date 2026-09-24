# generateContent

**Do tema ao carrossel pronto em uma conversa.**

Um agente de IA que escreve carrosséis para Instagram sobre a fé católica. Você diz o tema, ele pesquisa, propõe os hooks, escreve slide por slide no estilo do criador que você escolher e, com o texto aprovado, gera as imagens.

## Por que existe

Fazer um bom carrossel toma tempo: apurar os fatos, achar o gancho do primeiro slide, manter a voz de um estilo e ainda produzir a arte de cada slide. O generateContent junta essas etapas em um fluxo só, com você aprovando cada passo.

## Como o agente trabalha

1. **Pesquisa.** Busca na web fatos, contexto histórico, citações bíblicas e ditos de santos, e entrega um relatório para você revisar.
2. **Estilo.** Você escolhe qual criador ele deve imitar. Os exemplos vêm das transcrições dos vídeos que você colocar na base.
3. **Hooks.** Ele sugere pelo menos 10 títulos para o slide 1, feitos para prender a atenção em cerca de 3 segundos.
4. **Carrossel.** Com o hook escolhido, escreve de 7 a 12 slides, cada um com uma ideia e um gancho para o próximo.
5. **Imagens.** Depois que você aprova o texto, gera uma imagem vertical por slide (arte sacra, vitral, gravura), sem texto embutido, deixando espaço livre para a legenda.

Só entram no carrossel citações, datas e fatos confirmados na pesquisa. Toda a conduta do agente está em [prompts/copywriter.md](prompts/copywriter.md); edite esse arquivo para mudar o nicho, o tom ou os estilos.

## O que tem no projeto

| Arquivo | O que faz |
|---|---|
| [agent.py](agent.py) | O agente copywriter (Agno + DeepSeek), servido em uma interface web. O histórico fica em `tpmstorage.db`. |
| [tools.py](tools.py), [transcripter.py](transcripter.py) | Transcrevem os vídeos de `videos/<criador>/` com Whisper (Groq) e salvam em `transcricoes/`. |
| [imagem.py](imagem.py) | Gera as imagens dos slides (1024x1536) com a API de imagens da OpenAI. |
| [baixar_imagens.py](baixar_imagens.py) | Baixa posts do Instagram listados em `links_imagens.txt` para usar como referência visual. |
| [heygen.py](heygen.py) | Gera vídeo de um avatar falando um texto (HeyGen). |

## Começando

Você precisa de Python 3.13+, [Poetry](https://python-poetry.org/) e [FFmpeg](https://ffmpeg.org/) no PATH.

```bash
git clone <url-do-repositorio>
cd generateContent
make install
cp .env.example .env    # no Windows: copy .env.example .env
```

Preencha o `.env` com as chaves dos serviços que for usar:

| Variável | Para quê | Onde obter |
|---|---|---|
| `DEEPSEEK_API_KEY` | Modelo do agente | platform.deepseek.com |
| `TAVILY_API_KEY` | Pesquisa na web | tavily.com |
| `GROQ_API_KEY` | Transcrição dos vídeos | console.groq.com |
| `OPENAI_API_KEY` | Geração de imagens | platform.openai.com |
| `HEYGEN_API_KEY` | Vídeo com avatar | heygen.com |

Rode o agente:

```bash
poetry run python agent.py
```

O servidor sobe em `http://localhost:7777` e o terminal mostra o link para abrir o Playground em [app.agno.com/playground](https://app.agno.com/playground). Peça um carrossel, por exemplo: *"Quero um carrossel sobre São Padre Pio."*

## Ensinando um estilo ao agente

Quanto mais exemplos, mais fiel fica a imitação.

1. Coloque os vídeos `.mp4` de cada criador em `videos/<criador>/`.
2. Rode `make transcribe`.

As transcrições ficam em `transcricoes/<criador>.json` e o agente passa a consultá-las.

Para reunir referências visuais, liste os posts em `links_imagens.txt` (um por linha: link e nome da pasta) e rode `poetry run python baixar_imagens.py`.

## Segurança e privacidade

- As chaves ficam só no `.env`, que não vai para o Git. O código as lê de variáveis de ambiente e não contém nenhuma chave.
- Se uma chave vazar, revogue e gere outra no painel do serviço.
- O `tpmstorage.db` guarda o histórico das conversas e também fica fora do Git.
- Vídeos, transcrições e imagens de referência são conteúdo de terceiros e não são versionados. Respeite os direitos autorais e os termos de cada plataforma.

## Licença

MIT. Veja [LICENSE](LICENSE).
