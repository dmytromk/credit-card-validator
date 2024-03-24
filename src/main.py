from fastapi import FastAPI
from pydantic import ValidationError

from models.api_response import ValidationResponse
from models.card import Card

app = FastAPI()


@app.post("/validate/")
async def validate(card: dict):
    try:
        Card.model_validate(card)
        return ValidationResponse(valid=True)
    except ValidationError as e:
        return ValidationResponse.fromerrors(e)
