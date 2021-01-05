from decimal import Decimal
from typing import Dict, Optional, Union

from .data_classes import Response, ShopperCardData, ListCardResponse, WalletBalanceResponse


class ShopperPaymentsClientAdapter:
    def list_cards(self) -> ListCardResponse:
        raise NotImplementedError

    def assign_card(
        self, card_number_id: str, shopper_card_data: ShopperCardData
    ) -> Optional[Response]:
        raise NotImplementedError

    def get_card_balance(self, card_issuer_id: str) -> Optional[Response]:
        raise NotImplementedError

    def load_card(
        self, card_issuer_id: str, amount: Union[Decimal, float, str]
    ) -> Optional[Response]:
        raise NotImplementedError

    def unload_card(
        self, card_issuer_id, amount: Union[Decimal, float, str]
    ) -> Optional[Response]:
        raise NotImplementedError

    def activate_card(self, card_issuer_id) -> Optional[Response]:
        raise NotImplementedError

    def deactivate_card(self, card_issuer_id) -> Optional[Response]:
        raise NotImplementedError

    def wallet_balance(self) -> Optional[Response]:
        raise NotImplementedError

    def response_to_check(self, data: Dict[str, Union[str, int, Dict]]) -> Response:
        raise NotImplementedError

    def response_wallet_balance(
        self, data: Dict[str, Union[str, int, Dict]]
    ) -> WalletBalanceResponse:
        raise NotImplementedError

    def response_card_balance(self, data: Dict[str, Union[str, int, Dict]]) -> Response:
        raise NotImplementedError

    def response_list_cards(self, data: Dict[str, Union[str, int, Dict]]) -> Response:
        raise NotImplementedError

    def external_service_is_healthy(self):
        raise NotImplementedError
