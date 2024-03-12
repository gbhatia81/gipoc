from google.cloud import bigquery
from sqlalchemy import *
from sqlalchemy.engine import create_engine
from sqlalchemy.schema import *
import os
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase
from langchain.llms.openai import OpenAI
from langchain.agents import AgentExecutor
service_account_file = "/path/to/your/service-account-key.json" # Change to where your service account key file is located
project = "devopsandmore"
dataset = "langchain_test"
table = "churn_table"

sqlalchemy_url = f'bigquery://{project}/{dataset}'
# OpenAI API key
os.environ["OPENAI_API_KEY"] = "sk-secretxxxxx"
# Set up langchain
db = SQLDatabase.from_uri(sqlalchemy_url)
llm = OpenAI(temperature=0, model="text-davinci-003")
toolkit = SQLDatabaseToolkit(db=db, llm=llm)
agent_executor = create_sql_agent(
llm=llm,
toolkit=toolkit,
verbose=True,
top_k=1000,
)
# First query
agent_executor.run("How many male users churned? ")
# Second query
agent_executor.run("""How many users churned which had internet service?
How many churned which had no internet service?
And for each of the groups, how many did not churn?""")