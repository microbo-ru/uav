import streamlit as st
from agno.models.openai import OpenAIChat
from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.tools.duckdb import DuckDbTools

st.title('🧠 Ассистент по аналитике полетов')

#todo: make file selection dynamic
PROMPT="""
    
    Ты ассистент, который позволяет анализировать табличные данные.
    Используй базу знаний для поиска ответа.
    Всегда отвечай на русском языке.
"""

user_1_id = "user_101"
user_1_session_id = "session_101"
db = SqliteDb(db_file="tmp/data.db")

# CsvTools
# duckdb_tools = DuckDbTools()
# duckdb_tools.create_table_from_path(
#     path="https://agno-public.s3.amazonaws.com/demo_data/IMDB-Movie-Data.csv",
#     table="movies",
# )

duckdb_tools = DuckDbTools()
duckdb_tools.create_table_from_path(
    path="tmp/2024_Санкт-Петербург.csv",
    table="flights",
)

agent = Agent(
    model=OpenAIChat(id="GigaChat-2-Max", 
                        base_url="http://localhost:8090",
                        role_map={
                            "system": "system",
                            "user": "user",
                            "assistant": "assistant", 
                            "tool": "tool",
                            "model": "assistant",
                            "developer": "system",
                            "expert": "assistant"
                    }
    ),
    db=db,
    # add_history_to_context=True,
    # num_history_runs=3,
    # knowledge=knowledge,
    tools=[duckdb_tools],
    add_knowledge_to_context=True,
    search_knowledge=False,
    reasoning=False,
    instructions=PROMPT
)


with st.form("my_form"):
    query = st.text_area('Задайте свой вопрос:', 
"""Сколько полетов было выполнено на дату 2024-05-30 00:00:00?""", 
                         height=100)
    submitted = st.form_submit_button("🚀 Выполнить")

    if submitted:
        if query:
            st.markdown("### 💡 Ответ")
            answer_container = st.container()
            answer_placeholder = answer_container.empty()
            answer_text = ""
            
            with st.spinner("🔍 Поиск ответа..."):
                for chunk in agent.run(
                    query,
                    stream=True,
                    # user_id=user_1_id,
                    # session_id=user_1_session_id,
                ):
                    if hasattr(chunk, 'event') and chunk.event == "RunContent":
                        if hasattr(chunk, 'content') and chunk.content and isinstance(chunk.content, str):
                            answer_text += chunk.content
                            answer_placeholder.markdown(
                                answer_text, 
                                unsafe_allow_html=True
                            )
        else:
            st.error("Пожалуйста, введите вопрос.")