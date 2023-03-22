from sanic.blueprints import Blueprint
from .ads import ads
from .s3_ops import s3_ops

blueprints = Blueprint.group(ads, s3_ops)
