from langchain_google_vertexai import ChatVertexAI
from langchain.globals import set_verbose,set_debug

# set_verbose(True)
# set_debug(True)

llm = ChatVertexAI(model="gemini-1.5-pro", temperature=0.9)

from typing import Optional

from langchain_core.pydantic_v1 import BaseModel, Field


class Joke(BaseModel):
    """Joke to tell user."""

    setup: str = Field(description="The setup of the joke")
    punchline: str = Field(description="The punchline to the joke")
    rating: Optional[int] = Field(description="How funny the joke is, from 1 to 10")

class Add(BaseModel):
    """Add two integers together."""

    a: int = Field(..., description="First integer")
    b: int = Field(..., description="Second integer")


class Multiply(BaseModel):
    """Multiply two integers together."""

    a: int = Field(..., description="First integer")
    b: int = Field(..., description="Second integer")

from langchain_core.tools import tool


@tool
def add(a: int, b: int) -> int:
    """Adds a and b."""
    return a + b


@tool
def multiply(a: int, b: int) -> int:
    """Multiplies a and b."""
    return a * b

tools =[add,multiply]
llm_with_tools = llm.bind_tools(tools)
# llm_with_tools.invoke("What is 3 * 12? Also, what is 11 + 49?");
from langchain_core.messages import HumanMessage, ToolMessage

query = "What is 3 * 12? Also, what is 11 + 49?"

messages = [HumanMessage(query)]

ai_msg = llm_with_tools.invoke(query)
print(ai_msg.tool_calls)

messages.append(ai_msg)
for tool_call in ai_msg.tool_calls:
    selected_tool = {"add": add, "multiply": multiply}[tool_call["name"].lower()]
    tool_output = selected_tool.invoke(tool_call["args"])
    messages.append(ToolMessage(tool_output, tool_call_id=tool_call["id"]))
print(messages)
response = llm_with_tools.invoke(messages)
print(response)


# structured_llm = llm.with_structured_output(Joke)
# json_schema = {
#     "title": "joke",
#     "description": "Joke to tell user.",
#     "type": "object",
#     "properties": {
#         "setup": {
#             "type": "string",
#             "description": "The setup of the joke",
#         },
#         "punchline": {
#             "type": "string",
#             "description": "The punchline to the joke",
#         },
#         "rating": {
#             "type": "integer",
#             "description": "How funny the joke is, from 1 to 10",
#         },
#     },
#     "required": ["setup", "punchline"],
# }
# structured_llm = llm.with_structured_output(json_schema)


# response = structured_llm.invoke("Tell me a joke about cats")
# print(f"response is {response.content}")

