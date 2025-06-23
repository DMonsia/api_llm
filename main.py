from typing import Annotated
from fastapi import FastAPI, HTTPException, UploadFile, Body

from src.chain import invoke
from src.prompts import summary_prompt_template, chat_prompt
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

    response = invoke(query=summary_prompt_template.invoke(input={"content": content}))

    return {
        "filename": file.filename,
        "summary": response.content,
    }


@app.post("/chat")
def chat(messages: Annotated[list[dict[str, str]], Body()]):
    prompt = chat_prompt.invoke(input={"messages": messages})

    response = invoke(prompt)
    return {"role": "assistant", "content": response.content}
