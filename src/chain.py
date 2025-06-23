from langchain.chat_models import init_chat_model
from langchain_core.output_parsers.string import StrOutputParser

import configs

model = init_chat_model(
    model="gpt-4o",
    temperature=1.5,
    model_provider="openai",
    api_key=configs.OPENAI_API_KEY,
)


def get_chain(prompt):
    return prompt | model | StrOutputParser()
