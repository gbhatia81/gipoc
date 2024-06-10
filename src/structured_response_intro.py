from langchain_google_vertexai import ChatVertexAI
from langchain.globals import set_verbose,set_debug
from langchain_core.messages import HumanMessage

# set_verbose(True)
set_debug(True)

llm = ChatVertexAI(model="gemini-1.5-pro", temperature=0.9)

from typing import Optional

from langchain_core.pydantic_v1 import BaseModel, Field


class Joke(BaseModel):
    """Joke to tell user."""

    setup: str = Field(description="The setup of the joke")
    punchline: str = Field(description="The punchline to the joke")
    rating: Optional[int] = Field(description="How funny the joke is, from 1 to 10")

structured_llm = llm.with_structured_output(Joke)
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



response = structured_llm.invoke("Tell me a joke about cats")

print(f"response is {response}")