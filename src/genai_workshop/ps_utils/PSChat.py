#akschord1

from typing import Any, List, Mapping, Optional
from langchain.callbacks.manager import CallbackManagerForLLMRun
from langchain.llms.base import LLM
import requests
import os


def pschat(prompt,model="gpt4",max_token=5000,temperature="0.3",assistant=None) -> str:
    
    f = open('log.txt','a+')
    f.write('\n')
    f.write('-'*50)
    f.write('\n')
    f.write(str(prompt))
    f.write('\t'*5)
    f.write('*'*20)
    f.write('\n\n\n'+"output: \n\\n\n")
    
    url = 'https://api.psnext.info/api/chat'
    
    try:
        ps_chat_access_token = os.environ['PS_KEY']
    except KeyError:
        return "add PS_KEY environment variable os.environ['PS_KEY']"
        
    
    headers = {
        'Authorization': f'Bearer {ps_chat_access_token}',
        'Content-Type': 'application/json'
    }

    if assistant==None:

        data = {
            'message': str(prompt),
            'options': {
                'model': model,
                'max_token' : max_token,
                'temperature' : temperature

            }
        }
    else:
        data = {
            'message': prompt,
            'options': {
                'model': model,
                'max_token' : max_token,
                'temperature' : temperature,
                'assistant' : assistant

            }
        }
        
    
    
    
    try:
        response = requests.post(url, json=data, headers=headers)
        
    except Exception:
        print(Exception)
        return ''

    try:
        
        # print(str(response.json()['data']['messages'][-1]['content']))
        f.write(str(response.json()['data']['messages'][-1]['content']))
        f.close()
        return str(response.json()['data']['messages'][-1]['content'])
        
    except Exception:
        f.write(response.text)
        f.close()
        return response.text
        
    



"""PS Chat LLM Wrapper."""

class PSChat(LLM):
    model: Optional[str]
    max_token : Optional[int]
    temperature : Optional[float]
    

    @property
    def _llm_type(self) -> str:
        return "PS Chat"

    def _call(
        self,
        prompt: str,
        
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        # if stop is not None:
        #     raise ValueError("stop kwargs are not permitted.")
        return pschat(prompt,model=self.model,max_token = self.max_token,temperature = self.temperature)

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """Get the identifying parameters."""
        return {"model": self.model}
    
    

    







    """PS Chat Chat Wrapper."""
from typing import Any, List, Optional
from langchain_core.callbacks.manager import (
    AsyncCallbackManagerForLLMRun,
    CallbackManagerForLLMRun,
)
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import (
    AIMessage,
    BaseMessage,
    HumanMessage,
    SystemMessage,
)
from langchain_core.outputs import (
    ChatGeneration,
    ChatResult,
    LLMResult,
)


from typing import Any, Dict, List, Mapping, Optional
from langchain.callbacks.manager import CallbackManagerForLLMRun
from langchain.llms.base import LLM
from langchain.llms.utils import enforce_stop_tokens

from langchain.schema import (
    HumanMessage,
    SystemMessage,
)

import time

DEFAULT_SYSTEM_PROMPT = """You are a helpful, respectful, and honest assistant."""



class PS_Chat_model(BaseChatModel):

    llm: Any
    system_message: SystemMessage = SystemMessage(content=DEFAULT_SYSTEM_PROMPT)

    def __init__(self, task="text-generation"):
        super().__init__()
        self.llm = PSChat()

    def _generate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> ChatResult:
        llm_input = self._to_chat_prompt(messages)
        llm_result = self.llm._generate(
            prompts=llm_input, stop=stop, run_manager=run_manager, **kwargs
        )
        return self._to_chat_result(llm_result)

    def _to_chat_prompt(
        self,
        messages: List[BaseMessage],
    ) -> str:
        """Convert a list of messages into a prompt format expected by wrapped LLM."""
        if not messages:
            raise ValueError("at least one HumanMessage must be provided")

        if not isinstance(messages[-1], HumanMessage):
            raise ValueError("last message must be a HumanMessage")

        messages_dicts = [self._to_chatml_format(m) for m in messages]
        # print(messages_dicts)
        return messages_dicts

    @staticmethod
    def _to_chat_result(llm_result: LLMResult) -> ChatResult:
        chat_generations = []

        for g in llm_result.generations[0]:
            chat_generation = ChatGeneration(
                message=AIMessage(content=g.text), generation_info=g.generation_info
            )
            chat_generations.append(chat_generation)

        return ChatResult(
            generations=chat_generations, llm_output=llm_result.llm_output
        )

    @property
    def _llm_type(self) -> str:
        return "PS Chat model"

    def _to_chatml_format(self, message: BaseMessage) -> dict:
        """Convert LangChain message to ChatML format."""

        if isinstance(message, SystemMessage):
            role = "system"
        elif isinstance(message, AIMessage):
            role = "assistant"
        elif isinstance(message, HumanMessage):
            role = "user"
        else:
            raise ValueError(f"Unknown message type: {type(message)}")

        return {"role": role, "content": message.content}

    

    