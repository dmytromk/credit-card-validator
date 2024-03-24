import pytest
from datetime import date

from src.models.card import Card

NEXT_YEAR = str(date.today().year + 1)
PREVIOUS_YEAR = str(date.today().year - 1)


@pytest.mark.parametrize("card_number, expiration_month, expiration_year, expected_result", [
    ("4111111111111111", "01", NEXT_YEAR, True),
    ("5555555555554444", "01", NEXT_YEAR, True),
    ("6200000000000005", "01", NEXT_YEAR, True),
    ("   4111111111111111    ", "01", NEXT_YEAR, True),

    # Invalid card numbers
    ("4111111111111112", "01", NEXT_YEAR, False),  # Invalid Luhn check
    ("4111111111111111", "13", NEXT_YEAR, False),  # Invalid expiration month
    ("4111111111111111", "01", "1800", False),  # Past expiration year
    ("411111111111", "01", NEXT_YEAR, False),  # Invalid length
    ("1234567890123456", "01", NEXT_YEAR, False),  # Unknown issuer
    ("41111111111111", "01", NEXT_YEAR, False),  # Invalid length
    ("4111111111111111", "01", PREVIOUS_YEAR, False),  # Expired card


    ("5555555555554444", "01", " " + NEXT_YEAR + " ", True),

    ("4111111X111111111", "01", NEXT_YEAR, False),
    ("4111-1111-1111-1111", "01", NEXT_YEAR, False),

    ("4111111111111111", "0X", NEXT_YEAR, False),
    ("4111111111111111", "13", "20X9", False)
])
def test_card_validation(card_number, expiration_month, expiration_year, expected_result):
    card_data = {
        "Card number": card_number,
        "Expiration month": expiration_month,
        "Expiration year": expiration_year
    }

    if expected_result:
        Card(**card_data)
    else:
        with pytest.raises(Exception):
            Card(**card_data)
