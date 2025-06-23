from langchain.chat_models import init_chat_model

import configs

model = init_chat_model(
    model="gpt-4o",
    temperature=1.5,
    model_provider="openai",
    api_key=configs.OPENAI_API_KEY,
)


def invoke(query):
    return model.invoke(query)
