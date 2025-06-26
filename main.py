from typing import Annotated

from fastapi import Body, FastAPI, HTTPException, UploadFile
from langchain_core.output_parsers.json import JsonOutputParser
from langchain_core.output_parsers.string import StrOutputParser
from langchain_core.runnables import RunnableParallel

from src.chain import get_chain
from src.prompts import (
    automatic_answer_prompt,
    chat_prompt,
    information_extraction_prompt,
    summary_prompt_template,
)
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

    chain = get_chain(summary_prompt_template, StrOutputParser())
    return {
        "filename": file.filename,
        "summary": chain.invoke(input={"content": content}),
    }


@app.post("/chat")
def chat(messages: Annotated[list[dict[str, str]], Body()]):
    chain = get_chain(chat_prompt, StrOutputParser())
    return {"role": "assistant", "content": chain.invoke(input={"messages": messages})}


@app.get("/information_extraction")
def information_extraction(query: str):
    extract_chain = get_chain(
        prompt=information_extraction_prompt, parser=JsonOutputParser()
    )
    answer_chain = get_chain(automatic_answer_prompt, StrOutputParser())
    map_chain = RunnableParallel(
        structured_information=extract_chain, automatic_answer=answer_chain
    )
    return map_chain.invoke({"query": query})
