import time
from sanic import Sanic
from sanic.log import logger

from torpedo import CONFIG

from torpedo.constants import X_VISITOR_ID

config = CONFIG.config


def get_app():
    return Sanic.get_app(config["NAME"])


def get_x_visitor_id_from_request_headers(request_headers):
    x_visitor_id = None
    if X_VISITOR_ID.value in request_headers:
        x_visitor_id = request_headers[X_VISITOR_ID.value]
    return x_visitor_id


def log_combined_error(title, error):
    request_params = {"exception": error}
    logger.error(title, extra=request_params)
    combined_error = title + " " + error
    logger.info(combined_error)


def log_combined_exception(title, exception, meta_info: str = ""):
    error = "Exception type {} , exception {} , meta_info {}".format(
        type(exception), exception, str(meta_info)
    )
    log_combined_error(title, error)


def service_client_wrapper(service_name):
    def wrapped(func):
        async def wrapper(*args):
            try:
                t1 = time.time() * 1000
                response = await func(*args)
                t2 = time.time() * 1000
                logger.info(
                    "Time taken for {}-{} API - {} ms".format(
                        service_name, func.__name__, t2 - t1
                    )
                )
                return response
            except Exception as exception:
                log_combined_exception(
                    "Unable to get response from {}-{} API".format(
                        service_name, func.__name__
                    ),
                    exception,
                    "handled in service client wrapper",
                )

        return wrapper

    return wrapped
