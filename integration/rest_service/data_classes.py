from dataclasses import dataclass
from decimal import Decimal
from typing import List, Union


@dataclass
class ShopperCardData:
    name: str
    gender: str
    id_number: str
    birthdate: str
    phone_number: str
    email: str
    card_id: str
    pin_number: str = None
    month: str = None
    year: str = None
    cvv: str = None


@dataclass
class ErrorDetail:
    code: str
    message: str


@dataclass
class CardBalanceResponse:
    balance: Union[Decimal, float, str]


@dataclass
class CardResponse:
    card_number_id: str
    card_issuer_id: str
    card_status: str = None
    last_four_digits: str = None


@dataclass
class ListCardResponse:
    cards: List[CardResponse]


@dataclass
class WalletBalanceResponse:
    amount: Union[Decimal, float, str]
    currency: str
    country: str


@dataclass
class Response:
    status: str
    data: Union[
        CardBalanceResponse, CardResponse, ListCardResponse, WalletBalanceResponse
    ] = None
    error_details: List[ErrorDetail] = None
