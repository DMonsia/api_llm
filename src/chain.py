from openai import OpenAI

import configs

client = OpenAI(api_key=configs.OPENAI_API_KEY)


def invoke(query):
    return client.responses.create(
        model="gpt-4o", input=[{"role": "user", "content": query}]
    )
