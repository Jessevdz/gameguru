import requests
import json
from fastapi import FastAPI
from pydantic import BaseModel
from vector_db import VectorDB
from pdf import chunk_text


app = FastAPI()
db = VectorDB()


class Game(BaseModel):
    game_name: str
    game_rules: str


class Question(BaseModel):
    game: str
    user_query: str


@app.get("/games/list")
async def list_games() -> str:
    return db.list_games()


@app.post("/games/add")
async def add_game(game: Game) -> str:
    game_name = game.game_name
    game_rules = game.game_rules
    game_rules_chunks = chunk_text(game_rules)
    db.add(game_name, game_rules_chunks)
    return "Sucessfully added game to database"


@app.post("/answer")
async def question_handler(question: Question) -> str:
    game = question.game
    query = question.user_query
    relevant_documents = db.get_related_documents(game=game, query=query)
    # Send request to model API
    data = {"question": query, "game": game, "context_info": relevant_documents}
    response = requests.post(
        url="http://model:8000/complete_prompt", data=json.dumps(data)
    ).content.decode("utf-8")
    return response
