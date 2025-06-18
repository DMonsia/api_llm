from openai import OpenAI

import configs

client = OpenAI(api_key=configs.OPENAI_API_KEY)


def qa_invoke(query, instruction_prompt):
    return client.responses.create(
        instructions=instruction_prompt,
        model="gpt-4o",
        input=[{"role": "user", "content": query}],
    )


def chat_invoke(messages: list[dict[str, str]]):
    return client.responses.create(
        model="gpt-4o",
        input=messages,
    )
