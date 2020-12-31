import json
import logging
from json import JSONDecodeError
from os import getenv

import sentry_sdk
from flask import Flask, jsonify, request

from integration.rest_service.adapters import ShopperPaymentsClientAdapter
from integration.rest_service.data_classes import ErrorDetail, Response, ShopperCardData
from integration.rest_service.providers.exceptions import (
    GenericAPIException,
)

from .middlewares import AuthorizationMiddleware

logger = logging.getLogger(__name__)


ENVIRONMENT = getenv("FLASK_ENVIRONMENT", "local")
SENTRY_DSN = getenv("SENTRY_DSN", None)

if SENTRY_DSN:
    sentry_sdk.init(
        SENTRY_DSN,
        environment=ENVIRONMENT,
    )


def run_app(cls):
    assert issubclass(
        cls, ShopperPaymentsClientAdapter
    ), "adapter requires to extend from ShopperPaymentClientAdapter class"
    shopper_payments_adapter = cls()

    app = Flask(__name__)
    app.wsgi_app = AuthorizationMiddleware(app.wsgi_app)

    def get_error_response(e, code):
        try:
            error_message = e.error_message.decode()
        except AttributeError:
            error_message = e.error_message
        return jsonify(
            Response(
                error_details=[ErrorDetail(code=e.error_code, message=error_message)],
                status=code
            )
        )

    def get_logger_data(exception):
        data = {
            "data": {
                "provider": shopper_payments_adapter.name,
            }
        }
        message = exception.message if hasattr(exception, 'message') else None
        if message:
            try:
                data["data"]["detail"] = json.loads(message)
            except (TypeError, JSONDecodeError):
                data["data"]["detail"] = str(message)

        return data

    @app.route(f"/cards", methods=["GET"])
    def list_cards():
        try:
            response_data = shopper_payments_adapter.list_cards()
        except GenericAPIException as e:
            logger.info(f"Shopper payments integration (list_cards) request error {e.error_message}",
                        extra=get_logger_data(e))
            return get_error_response(e, 400)
        return response_data

    @app.route(f"/wallet/balance", methods=["GET"])
    def wallet_balance():
        try:
            response_data = shopper_payments_adapter.wallet_balance()
        except GenericAPIException as e:
            logger.info(f"Shopper payments integration (wallet_balance) request error {e.error_message}",
                        extra=get_logger_data(e))
            return get_error_response(e, 400)
        return response_data

    @app.route(f"/card/<card_issuer_id>/balance", methods=["GET"])
    def get_card_balance(card_issuer_id):
        try:
            response_data = shopper_payments_adapter.get_card_balance(
                card_issuer_id=card_issuer_id
            )
        except GenericAPIException as e:
            logger.info(f"Shopper payments integration (get_card_balance) request error {e.error_message}",
                        extra=get_logger_data(e))
            return get_error_response(e, 400)
        return response_data

    @app.route(f"/card/<card_issuer_id>/load", methods=["POST"])
    def load_card(card_issuer_id):
        data = json.loads(request.data)
        try:
            response_data = shopper_payments_adapter.load_card(
                card_issuer_id=card_issuer_id, amount=data.get("amount")
            )
        except GenericAPIException as e:
            logger.info(f"Shopper payments integration (load_card) request error {e.error_message}",
                        extra=get_logger_data(e))
            return get_error_response(e, 400)
        return response_data

    @app.route(f"/card/<card_issuer_id>/unload", methods=["POST"])
    def unload_card(card_issuer_id):
        data = json.loads(request.data)
        try:
            response_data = shopper_payments_adapter.unload_card(
                card_issuer_id=card_issuer_id, amount=data.get("amount")
            )
        except GenericAPIException as e:
            logger.info(f"Shopper payments integration (unload_card) request error {e.error_message}",
                        extra=get_logger_data(e))
            return get_error_response(e, 400)
        return response_data

    @app.route(f"/card/<card_number_id>/assign", methods=["POST"])
    def assign_card(card_number_id):
        data = json.loads(request.data)
        shopper_card_data = ShopperCardData(
            email=data.get("email"),
            name=data.get("name"),
            gender=data.get("gender"),
            id_number=data.get("id_number"),
            birthdate=data.get("birthdate"),
            phone_number=data.get("phone_number"),
            pin_number=data.get("pin_number"),
            month=data.get("month"),
            year=data.get("year"),
            cvv=data.get("ccv"),
        )

        try:
            response_data = shopper_payments_adapter.assign_card(
                card_number_id=card_number_id, shopper_card_data=shopper_card_data
            )
        except GenericAPIException as e:
            logger.info(f"Shopper payments integration (assign_card) request error {e.error_message}",
                        extra=get_logger_data(e))
            return get_error_response(e, 400)
        return response_data

    @app.route(f"/card/<card_issuer_id>/activate", methods=["POST"])
    def activate_card(card_issuer_id):
        try:
            response_data = shopper_payments_adapter.activate_card(
                card_issuer_id=card_issuer_id
            )
        except GenericAPIException as e:
            logger.info(f"Shopper payments integration (activate_card) request error {e.error_message}",
                        extra=get_logger_data(e))
            return get_error_response(e, 400)
        return response_data

    @app.route(f"/card/<card_issuer_id>/deactivate", methods=["POST"])
    def deactivate_card(card_issuer_id):
        try:
            response_data = shopper_payments_adapter.deactivate_card(
                card_issuer_id=card_issuer_id
            )
        except GenericAPIException as e:
            logger.info(f"Shopper payments integration (deactivate_card) request error {e.error_message}",
                        extra=get_logger_data(e))
            return get_error_response(e, 400)
        return response_data

    @app.route(f"/healthz", methods=["GET"])
    def health():
        return {}, 200

    # External integration's health
    @app.route(f"/external_health", methods=["GET"])
    def external_health():
        if shopper_payments_adapter.external_service_is_healthy():
            return {}, 200
        return {}, 503

    return app
