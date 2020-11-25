# -*- coding: utf-8 -*-
from integration.rest_service.exceptions import GenericAPIException


class GenericAPIException(GenericAPIException):
    pass


class BadRequestAPIException(GenericAPIException):
    pass


class UnauthorizedAPIException(GenericAPIException):
    pass


class ForbiddenAPIException(GenericAPIException):
    pass


class NotFoundAPIException(GenericAPIException):
    pass


class UnprocessableEntityAPIException(GenericAPIException):
    pass
