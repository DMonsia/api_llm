from typing import Annotated
from fastapi import FastAPI, HTTPException, UploadFile, Body

from src.chain import get_chain
from src.prompts import summary_prompt_template, chat_prompt
from src.utils import read_pdf, read_text

app = FastAPI(
    title="API LLM", description="Handle OpenAI API for developer", version="0.0.1"
)


@app.get("/")
def api_llm():
    return {"message": "welcom!"}


@app.post("/summary/")
async def get_summary(file: UploadFile):
    if file.content_type == "text/plain":
        content = read_text(file=file.file)
    elif file.content_type == "application/pdf":
        content = read_pdf(file.file)
    else:
        raise HTTPException(
            status_code=500, detail="Only '.pdf' and '.txt' files are supported."
        )

    chain = get_chain(summary_prompt_template)
    return {
        "filename": file.filename,
        "summary": chain.invoke(input={"content": content}),
    }


@app.post("/chat")
def chat(messages: Annotated[list[dict[str, str]], Body()]):
    chain = get_chain(chat_prompt)
    return {"role": "assistant", "content": chain.invoke(input={"messages": messages})}
