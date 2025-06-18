from typing import Annotated
from fastapi import FastAPI, HTTPException, UploadFile, Body

from src.chain import chat_invoke, qa_invoke
from src.prompts import summary_prompt, instruction_summary, chat_prompt
from src.utils import read_pdf, read_text

app = FastAPI(
    title="API LLM", description="Handle OpenAI API for developper", version="0.0.1"
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

    response = qa_invoke(
        query=summary_prompt.format(content=content),
        instruction_prompt=instruction_summary,
    )

    return {
        "filename": file.filename,
        "summary": response.output_text,
    }


@app.post("/chat")
def chat(messages: Annotated[list[dict[str, str]], Body()]):
    messages = [{"role": "developer", "content": chat_prompt}] + messages

    response = chat_invoke(messages)
    return {"role": "assistant", "content": response.output_text}
