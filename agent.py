from dotenv import load_dotenv

from agno.agent import Agent
from agno.models.deepseek import DeepSeek
from agno.playground import Playground, serve_playground_app
from agno.storage.sqlite import SqliteStorage
from agno.tools.tavily import TavilyTools

from heygen import generate_avatar_video, list_avatars
from imagem import gerar_imagem
from tools import create_transcriptions, get_transcriptions

load_dotenv()

copywriter = Agent(
    name="copywriter",
    model=DeepSeek(id="deepseek-chat"),
    tools=[TavilyTools(), get_transcriptions, create_transcriptions, list_avatars, generate_avatar_video, gerar_imagem],
    add_history_to_messages=True,
    num_history_runs=10,
    show_tool_calls=True,
    instructions=open("prompts/copywriter.md", encoding="utf-8").read(),
    storage=SqliteStorage(table_name="agent_session", db_file="tpmstorage.db"),
)

app = Playground(agents=[copywriter]).get_app()

if __name__ == "__main__":
    serve_playground_app("agent:app", reload=True)
