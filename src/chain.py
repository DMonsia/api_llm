from langchain.chat_models import init_chat_model

import configs

model = init_chat_model(
    model="gpt-4o",
    temperature=0.5,
    model_provider="openai",
    api_key=configs.OPENAI_API_KEY,
)


def get_chain(prompt, parser):
    return prompt | model | parser
