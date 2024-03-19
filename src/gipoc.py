from google.cloud import bigquery
from sqlalchemy import *
from sqlalchemy.engine import create_engine
from sqlalchemy.schema import *
import os
# from langchain_community.agent_toolkits import create_sql_agent 
from langchain.agents import create_sql_agent
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from agent_toolkit.CustomSQLDatabaseToolkit import CustomSQLDatabaseToolkit
from langchain.sql_database import SQLDatabase

from langchain_google_vertexai import VertexAI
# from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor

# service_account_file = "/path/to/your/service-account-key.json" # Change to where your service account key file is located

project = "burner-gaubhati0"
dataset = "sample"
#table = "Sales"

sqlalchemy_url = f'bigquery://{project}/{dataset}'

# Set up langchain
db = SQLDatabase.from_uri(sqlalchemy_url,sample_rows_in_table_info=0)

# os.environ["OPENAI_API_KEY"] = "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"

llm = VertexAI(model_name="gemini-pro")
# llm = VertexAI()

# llm = ChatOpenAI(
#     model_name='text-davinci-003'
# )


toolkit = CustomSQLDatabaseToolkit(db=db, llm=llm)

# for tool in toolkit.get_tools():
#     print(f" tool name:{tool.name} | tool desc: {tool.description}")
    

agent_executor = create_sql_agent(
llm=llm,
toolkit=toolkit,
verbose=True,
top_k=1000,
)


# This is an important query which does not work well with nested BQ Table in Vertex but OpenAI seems to handle it.
# Use it with Sales_nested.json schema
#agent_executor.invoke("What are total actual sale price in store STORE_1 in month on January in year 2024? ")

#agent_executor.invoke("Show me sales for STORE_1 for Q1 2024? ")

# agent_executor.invoke("Show me sales for all stores for Q1 2024. "
#                       "Give me results as two columns with first column as store_id and second column as total sales "
#                       "separated by '|' character.")

# agent_executor.invoke("Show me sales for all stores for Q1 2024. Only query relevant columns in table."
#                       "Return the final response in json format. json Format shoud have message field with final response "
#                       "and data field with results of final response from database. Data field should contain field column_name with respective column name "
#                       "and field value with respective column value")

agent_executor.invoke("Show me sales for STORE_1 for Q1 2024? ")

