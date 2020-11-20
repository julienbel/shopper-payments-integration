import base64
import json
import logging
from json import JSONDecodeError
from os import getenv
import sentry_sdk

from flask import Flask, jsonify, request
from requests import Timeout
from .middlewares import AuthorizationMiddleware
from integration.rest_service.adapters import ShopperPaymentsClientAdapter
from integration.rest_service.constants import FAILED
from integration.rest_service.data_classes import ErrorDetail, Response, ShopperCardData
from integration.rest_service.providers.exceptions import (
    BadRequestAPIException,
    GenericAPIException,
    NotFoundAPIException,
)

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

    def get_logger_data(message=None):
        data = {
            "data": {
                "provider": shopper_payments_adapter.name,
            }
        }
        if message:
            try:
                data["data"]["detail"] = json.loads(message)
            except (TypeError, JSONDecodeError):
                data["data"]["detail"] = str(message)

        return data


    @app.route(f'/cards', methods=['GET'])
    def list_cards():
        try:
            response_data = shopper_payments_adapter.list_cards()
        except (Timeout, ConnectionError):
            logger.info("Shopper payments integration adapter timeout", extra=get_logger_data(check_data))
            return jsonify(
                Response(
                    status=FAILED,
                    error_details=[
                        ErrorDetail(
                            code="408", message=json.loads({"error": "Timeout"})
                        )
                    ],
                )
            )
        except (BadRequestAPIException, NotFoundAPIException) as e:
            logger.info(
                "Shopper payments integration adapter request exception",
                extra=get_logger_data(e.message),
            )
            return jsonify(
                Response(
                    status=FAILED,
                    error_details=[
                        ErrorDetail(code="400", message=json.loads(e.message))
                    ],
                )
            )
        except GenericAPIException as e:
            logger.info(
                "Shopper payments integration adapter generic exception",
                extra=get_logger_data(e.message),
            )
            return jsonify(
                Response(
                    status=FAILED,
                    error_details=[
                        ErrorDetail(code="500", message=json.loads(e.message))
                    ],
                )
            )
        return response_data


    @app.route(f'/wallet/balance', methods=['GET'])
    def wallet_balance():
        try:
            response_data = shopper_payments_adapter.wallet_balance()
        except (Timeout, ConnectionError):
            logger.info("Shopper payments integration adapter timeout", extra=get_logger_data())
            return jsonify(
                Response(
                    status=FAILED,
                    error_details=[
                        ErrorDetail(
                            code="408", message=json.loads({"error": "Timeout"})
                        )
                    ],
                )
            )
        except (BadRequestAPIException, NotFoundAPIException) as e:
            logger.info(
                "Shopper payments integration adapter request exception",
                extra=get_logger_data(e.message),
            )
            return jsonify(
                Response(
                    status=FAILED,
                    error_details=[
                        ErrorDetail(code="400", message=json.loads(e.message))
                    ],
                )
            )
        except GenericAPIException as e:
            logger.info(
                "Shopper payments integration adapter generic exception",
                extra=get_logger_data(check_data, e.message),
            )
            return jsonify(
                Response(
                    status=FAILED,
                    error_details=[
                        ErrorDetail(code="500", message=json.loads(e.message))
                    ],
                )
            )
        return response_data


    @app.route(f'/card/<card_issuer_id>/balance', methods=['GET'])
    def get_card_balance(card_issuer_id):
        try:
            response_data = shopper_payments_adapter.get_card_balance(card_issuer_id=card_issuer_id)
        except (Timeout, ConnectionError):
            logger.info("Shopper payments integration adapter timeout", extra=get_logger_data())
            return jsonify(
                Response(
                    status=FAILED,
                    error_details=[
                        ErrorDetail(
                            code="408", message=json.loads({"error": "Timeout"})
                        )
                    ],
                )
            )
        except (BadRequestAPIException, NotFoundAPIException) as e:
            logger.info(
                "Shopper payments integration adapter request exception",
                extra=get_logger_data(e.message),
            )
            return jsonify(
                Response(
                    status=FAILED,
                    error_details=[
                        ErrorDetail(code="400", message=json.loads(e.message))
                    ],
                )
            )
        except GenericAPIException as e:
            logger.info(
                "Shopper payments integration adapter generic exception",
                extra=get_logger_data(e.message),
            )
            return jsonify(
                Response(
                    status=FAILED,
                    error_details=[
                        ErrorDetail(code="500", message=json.loads(e.message))
                    ],
                )
            )
        return response_data


    @app.route(f'/card/<card_issuer_id>/load', methods=['POST'])
    def load_card(card_issuer_id):
        data = json.loads(request.data)
        try:
            response_data = shopper_payments_adapter.load_card(card_issuer_id=card_issuer_id, amount=data.get("amount"))
        except (Timeout, ConnectionError):
            logger.info("Shopper payments integration adapter timeout", extra=get_logger_data())
            return jsonify(
                Response(
                    status=FAILED,
                    error_details=[
                        ErrorDetail(
                            code="408", message=json.loads({"error": "Timeout"})
                        )
                    ],
                )
            )
        except (BadRequestAPIException, NotFoundAPIException) as e:
            logger.info(
                "Shopper payments integration adapter request exception",
                extra=get_logger_data(e.message),
            )
            return jsonify(
                Response(
                    status=FAILED,
                    error_details=[
                        ErrorDetail(code="400", message=json.loads(e.message))
                    ],
                )
            )
        except GenericAPIException as e:
            logger.info(
                "Shopper payments integration adapter generic exception",
                extra=get_logger_data(e.message),
            )
            return jsonify(
                Response(
                    status=FAILED,
                    error_details=[
                        ErrorDetail(code="500", message=json.loads(e.message))
                    ],
                )
            )
        return response_data


    @app.route(f'/card/<card_issuer_id>/unload', methods=['POST'])
    def unload_card(card_issuer_id):
        data = json.loads(request.data)
        try:
            response_data = shopper_payments_adapter.unload_card(card_issuer_id=card_issuer_id, amount=data.get("amount"))
        except (Timeout, ConnectionError):
            logger.info("Shopper payments integration adapter timeout", extra=get_logger_data())
            return jsonify(
                Response(
                    status=FAILED,
                    error_details=[
                        ErrorDetail(
                            code="408", message=json.loads({"error": "Timeout"})
                        )
                    ],
                )
            )
        except (BadRequestAPIException, NotFoundAPIException) as e:
            logger.info(
                "Shopper payments integration adapter request exception",
                extra=get_logger_data(e.message),
            )
            return jsonify(
                Response(
                    status=FAILED,
                    error_details=[
                        ErrorDetail(code="400", message=json.loads(e.message))
                    ],
                )
            )
        except GenericAPIException as e:
            logger.info(
                "Shopper payments integration adapter generic exception",
                extra=get_logger_data(e.message),
            )
            return jsonify(
                Response(
                    status=FAILED,
                    error_details=[
                        ErrorDetail(code="500", message=json.loads(e.message))
                    ],
                )
            )
        return response_data


    @app.route(f'/card/<card_number_id>/assign', methods=['POST'])
    def assign_card(card_number_id):
        data = json.loads(request.data)
        shopper_card_data = ShopperCardData(email=data.get("email"),
                                            name=data.get("name"),
                                            gender=data.get("gender"),
                                            id_number=data.get("id_number"),
                                            birthdate=data.get("birthdate"),
                                            phone_number=data.get("phone_number"),
                                            pin_number=data.get("pin_number"),
                                            month=data.get("month"),
                                            year=data.get("year"),
                                            cvv=data.get("ccv"))

        try:
            response_data = shopper_payments_adapter.assign_card(card_number_id=card_number_id, shopper_card_data=shopper_card_data)
        except (Timeout, ConnectionError):
            logger.info("Shopper payments integration adapter timeout", extra=get_logger_data())
            return jsonify(
                Response(
                    status=FAILED,
                    error_details=[
                        ErrorDetail(
                            code="408", message=json.loads({"error": "Timeout"})
                        )
                    ],
                )
            )
        except (BadRequestAPIException, NotFoundAPIException) as e:
            logger.info(
                "Shopper payments integration adapter request exception",
                extra=get_logger_data(e.message),
            )
            return jsonify(
                Response(
                    status=FAILED,
                    error_details=[
                        ErrorDetail(code="400", message=json.loads(e.message))
                    ],
                )
            )
        except GenericAPIException as e:
            logger.info(
                "Shopper payments integration adapter generic exception",
                extra=get_logger_data(e.message),
            )
            return jsonify(
                Response(
                    status=FAILED,
                    error_details=[
                        ErrorDetail(code="500", message=json.loads(e.message))
                    ],
                )
            )
        return response_data


    @app.route(f'/card/<card_issuer_id>/activate', methods=['POST'])
    def activate_card(card_issuer_id):
        try:
            response_data = shopper_payments_adapter.activate_card(card_issuer_id=card_issuer_id)
        except (Timeout, ConnectionError):
            logger.info("Shopper payments integration adapter timeout", extra=get_logger_data())
            return jsonify(
                Response(
                    status=FAILED,
                    error_details=[
                        ErrorDetail(
                            code="408", message=json.loads({"error": "Timeout"})
                        )
                    ],
                )
            )
        except (BadRequestAPIException, NotFoundAPIException) as e:
            logger.info(
                "Shopper payments integration adapter request exception",
                extra=get_logger_data(e.message),
            )
            return jsonify(
                Response(
                    status=FAILED,
                    error_details=[
                        ErrorDetail(code="400", message=json.loads(e.message))
                    ],
                )
            )
        except GenericAPIException as e:
            logger.info(
                "Shopper payments integration adapter generic exception",
                extra=get_logger_data(e.message),
            )
            return jsonify(
                Response(
                    status=FAILED,
                    error_details=[
                        ErrorDetail(code="500", message=json.loads(e.message))
                    ],
                )
            )
        return response_data


    @app.route(f'/card/<card_issuer_id>/deactivate', methods=['POST'])
    def deactivate_card(card_issuer_id):
        try:
            response_data = shopper_payments_adapter.deactivate_card(card_issuer_id=card_issuer_id)
        except (Timeout, ConnectionError):
            logger.info("Shopper payments integration adapter timeout", extra=get_logger_data())
            return jsonify(
                Response(
                    status=FAILED,
                    error_details=[
                        ErrorDetail(
                            code="408", message=json.loads({"error": "Timeout"})
                        )
                    ],
                )
            )
        except (BadRequestAPIException, NotFoundAPIException) as e:
            logger.info(
                "Shopper payments integration adapter request exception",
                extra=get_logger_data(e.message),
            )
            return jsonify(
                Response(
                    status=FAILED,
                    error_details=[
                        ErrorDetail(code="400", message=json.loads(e.message))
                    ],
                )
            )
        except GenericAPIException as e:
            logger.info(
                "Shopper payments integration adapter generic exception",
                extra=get_logger_data(e.message),
            )
            return jsonify(
                Response(
                    status=FAILED,
                    error_details=[
                        ErrorDetail(code="500", message=json.loads(e.message))
                    ],
                )
            )
        return response_data


    @app.route(f'/healthz', methods=["GET"])
    def health():
        return {}, 200

    # External integration's health
    @app.route(f'/external_health', methods=["GET"])
    def external_health():
        if shopper_payments_adapter.external_service_is_healthy():
            return {}, 200
        return {}, 503

    return app