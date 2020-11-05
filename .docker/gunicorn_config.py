from os import getenv
import logging
from gunicorn import glogging

## Use "," as separator. Do not add a final ","
ACCESS_LOG_FILTERED_PATHS = [
    path for path in getenv("ACCESS_LOG_FILTERED_LOG", "/healthz").split(",")
]

bind = "0.0.0.0:8000"

worker_class = "gevent"
worker_connections = 100

timeout = 10
graceful_timeout = 10

if getenv("FLASK_ENV", "") == "development":
    reload = True

class AccessLogFilter(logging.Filter):
    def filter(self, record):
        for path in ACCESS_LOG_FILTERED_PATHS:
            if path in record.getMessage():
                return False
        return True


class CustomLogger(glogging.Logger):
    def setup(self, cfg):
        super().setup(cfg)
        logger = logging.getLogger("gunicorn.access")
        logger.addFilter(AccessLogFilter())


accesslog = "-"
errorlog = "-"
logger_class = CustomLogger