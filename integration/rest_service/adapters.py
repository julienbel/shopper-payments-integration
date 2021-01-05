from decimal import Decimal
from typing import Dict, Optional, Union

from .data_classes import (
    CardBalanceResponse,
    ListCardResponse,
    Response,
    ShopperCardData,
    WalletBalanceResponse,
)


class ShopperPaymentsClientAdapter:
    def list_cards(self) -> ListCardResponse:
        raise NotImplementedError

    def assign_card(
        self, card_number_id: str, shopper_card_data: ShopperCardData
    ) -> Response:
        raise NotImplementedError

    def get_card_balance(self, card_issuer_id: str) -> CardBalanceResponse:
        raise NotImplementedError

    def load_card(
        self, card_issuer_id: str, amount: Union[Decimal, float, str]
    ) -> Response:
        raise NotImplementedError

    def unload_card(
        self, card_issuer_id, amount: Union[Decimal, float, str]
    ) -> Response:
        raise NotImplementedError

    def activate_card(self, card_issuer_id) -> Response:
        raise NotImplementedError

    def deactivate_card(self, card_issuer_id) -> Response:
        raise NotImplementedError

    def wallet_balance(self) -> WalletBalanceResponse:
        raise NotImplementedError

    def response_wallet_balance(
        self, data: Dict[str, Union[str, int, Dict]]
    ) -> WalletBalanceResponse:
        raise NotImplementedError

    def response_card_balance(
        self, data: Dict[str, Union[str, int, Dict]]
    ) -> CardBalanceResponse:
        raise NotImplementedError

    def response_list_cards(
        self, data: Dict[str, Union[str, int, Dict]]
    ) -> ListCardResponse:
        raise NotImplementedError

    def external_service_is_healthy(self):
        raise NotImplementedError
