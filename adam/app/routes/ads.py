from sanic import Blueprint
from torpedo import send_response, Request


ads = Blueprint("ads", version=4)


@ads.route("/ping", methods=["GET"])
async def get_products(request: Request):
    """
    :param request:
    :return:
    """
    return send_response({"ping": "pong"})
