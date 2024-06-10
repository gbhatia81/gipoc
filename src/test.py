from langchain_core.prompts import ChatPromptTemplate
from langchain_google_vertexai import ChatVertexAI
from operator import itemgetter
from langchain_core.runnables import RunnablePassthrough
from langchain_core.runnables import RunnableLambda

model = ChatVertexAI(model="gemini-pro")
prompt = ChatPromptTemplate.from_template("Tell me {story} about a {thing}")

chain = {"story":RunnableLambda(lambda x : "story" ),"thing":RunnablePassthrough()} | prompt | model

chain.invoke("Animal")