from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain.chains import create_sql_query_chain
from langchain_community.llms import Ollama
from langchain_community.tools.sql_database.tool import QuerySQLDatabaseTool
from langchain_experimental.sql import SQLDatabaseChain
from langchain_community.utilities.sql_database import SQLDatabase
from sqlalchemy import create_engine
from langchain.sql_database import SQLDatabase
import streamlit as st

load_dotenv()

# OLLAMA_SERVER_URL="http://localhost:11434"
llm_model=Ollama(model="gemma3:4b", temperature=0.1)


def extract_sql(text):
    words_to_remove = ["SQLQuery:", "sql"]
    for word_to_remove in words_to_remove:
        text = text.replace(word_to_remove, "")
    text = text[text.find("SELECT"): text.find(";")]
    return text

def execute_user_query(llm=llm_model,db_name= any, question=any):

    POSTGRES_USER= st.secrets["db_name"]
    POSTGRES_PASSWORD=st.secrets["db_password"]
    POSTGRES_HOST= st.secrets["postgres_host"]
    POSTGRES_PORT= "57213"
    POSTGRES_DB=db_name
    connection_string = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    engine = create_engine(connection_string)
    db = SQLDatabase(engine)

    generate_query = create_sql_query_chain(llm,db)
    query=generate_query.invoke({"question": question})
    execute_query = QuerySQLDatabaseTool(db=db)
    cleaned_query = extract_sql(query)
    result = execute_query.invoke(cleaned_query)
    return cleaned_query,result