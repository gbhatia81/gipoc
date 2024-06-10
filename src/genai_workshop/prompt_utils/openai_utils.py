from openai import OpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI

OPEN_AI_MODEL_NAME = "gpt-3.5-turbo"
OPEN_AI_GPT3_16K_MODEL_NAME = "gpt-3.5-turbo-16k-0613"
OPEN_AI_MODEL_TEMPERATURE = 0


OPEN_SOURCE_EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


client = OpenAI()


def get_completion(prompt, model=OPEN_AI_MODEL_NAME):
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model=model, messages=messages, temperature=OPEN_AI_MODEL_TEMPERATURE
    )
    return response.choices[0].message.content


def get_completion_message(messages, model=OPEN_AI_MODEL_NAME):
    response = client.chat.completions.create(
        model=model, messages=messages, temperature=OPEN_AI_MODEL_TEMPERATURE
    )
    return response.choices[0].message.content


def openai_function_call(
    messages, my_function, my_function_call, model=OPEN_AI_MODEL_NAME
):
    response = client.chat.completions.create(
        model=model,
        temperature=OPEN_AI_MODEL_TEMPERATURE,
        messages=messages,
        functions=my_function,
        function_call=my_function_call,
    )

    return response.choices[0].message.function_call.arguments


def get_openai_chat_model():
    model = ChatOpenAI(
        model_name=OPEN_AI_MODEL_NAME,
        temperature=OPEN_AI_MODEL_TEMPERATURE,
        # verbose=True
    )
    return model


def get_openai_gpt3_16k_chat_model():
    return ChatOpenAI(
        temperature=OPEN_AI_MODEL_TEMPERATURE, model_name=OPEN_AI_GPT3_16K_MODEL_NAME
    )


def get_openai_embeddings():
    return OpenAIEmbeddings()


# def get_open_sourced_embeddings():
#     embeddings = HuggingFaceEmbeddings(
#         model_name=OPEN_SOURCE_EMBEDDING_MODEL, multi_process=True
#     )
#     return embeddings
