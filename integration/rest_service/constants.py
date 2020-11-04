from os import getenv

COMPLETED = 'COMPLETED'
PENDING = 'PENDING'
FAILED = 'FAILED'
ERROR = 'ERROR'
APPROVED = 'APPROVED'
REJECTED = 'REJECTED'
ACESSO_BR = 'ACESSO_BR'


GENDER = {"Masculino": "male", "Feminino": "female"}

APP_NAME = getenv("APP_NAME", "CS_SHOPPER_PAYMENT")
API_PATH = getenv("API_PATH", "/api")
