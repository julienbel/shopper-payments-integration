import base64
from werkzeug.wrappers import Request, Response
from os import getenv


class AuthorizationMiddleware:
    '''
    Simple WSGI middleware
    '''

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        request = Request(environ)
        signature = request.headers.get("Authorization")
        password = str(base64.b64decode(signature), "utf-8")

        if password != getenv("REQUEST_PASSWORD"):
            res = Response(u'Authorization failed', mimetype='text/plain', status=403)
            return res(environ, start_response)

        return self.app(environ, start_response)
