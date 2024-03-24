from calendar import monthrange
from datetime import date
from enum import Enum

from pydantic import BaseModel, Field, field_validator, model_validator, StringConstraints
from pydantic_core import PydanticCustomError
from typing_extensions import Annotated


class CardIssuer(Enum):
    MASTERCARD = "Mastercard"
    VISA = "Visa"
    UNIONPAY = "UnionPay"


class Card(BaseModel):
    card_number: Annotated[str, Field(alias="Card number")]

    expiration_month: Annotated[str, Field(alias="Expiration month"),
    StringConstraints(strip_whitespace=True, pattern="^(0?[1-9]|1[012])$")]  # 01-12

    expiration_year: Annotated[str, Field(alias="Expiration year"),
    StringConstraints(strip_whitespace=True, pattern="^(19|20)\d{2}$")]  # 1900-2099

    @model_validator(mode="after")
    def check_card_expiration(self) -> "Card":
        month, year = int(self.expiration_month), int(self.expiration_year)

        if date.today() > date(year, month, monthrange(year, month)[-1]):
            raise PydanticCustomError("card_expired", "Card is expired")

        return self

    @field_validator("card_number", mode="after")
    def validate_card_number(cls, v: str) -> str:
        v = v.strip()

        if not v.isdigit():
            raise PydanticCustomError("card_number_digits", "Card number must contain digits and only digits")

        Card.luhn_check(v)
        Card.issuer_check(v)

        return v

    @staticmethod
    def luhn_check(card_number: str) -> None:
        # https://en.wikipedia.org/wiki/Luhn_algorithm

        sum_result = 0
        for i, digit in enumerate(reversed(card_number)):
            n = int(digit)

            if i % 2 == 0:
                sum_result += n
            elif n >= 5:
                sum_result += n * 2 - 9
            else:
                sum_result += n * 2

        if not sum_result % 10 == 0:
            raise PydanticCustomError("card_number_luhn", "Card number failed Lunh check")

    @staticmethod
    def issuer_check(card_number: str) -> None:

        if card_number[0] == "4":
            issuer = CardIssuer.VISA
            required_length = [13, 16, 19]
        elif 51 <= int(card_number[:2]) <= 55:
            issuer = CardIssuer.MASTERCARD
            required_length = [16]
        elif card_number[:2] in ["62", "81"]:
            issuer = CardIssuer.UNIONPAY
            required_length = [16, 19]
        else:
            raise PydanticCustomError("card_number_unknown_issuer", "Card issuer can't be identified")

        if not len(card_number) in required_length:
            raise PydanticCustomError(
                "card_number_length",
                f"Card issued by {issuer} length must be {' or '.join(map(str, required_length))}"
            )
