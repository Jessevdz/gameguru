from typing import List
from fastapi import FastAPI
from pydantic import BaseModel
from llm import answer_question


app = FastAPI()


class PromptData(BaseModel):
    question: str
    game: str
    context_info: List[str]


@app.post("/complete_prompt")
async def complete_prompt(data: PromptData):
    response = answer_question(data.question, data.game, data.context_info)
    return response
