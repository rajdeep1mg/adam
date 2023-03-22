import io
import json
from sanic import Blueprint
from torpedo import Request, send_response
from managers.s3_manager import S3Manager


s3_ops = Blueprint("S3-Operations", version=4, url_prefix="/")


@s3_ops.post("/push-to-s3-bucket")
async def push_to_s3_bucket(request: Request):
    json_data = request.json
    data = json.dumps(json_data)
    response = await S3Manager.push_to_s3_bucket(data)
    return send_response(
        body={
            "message": "openapi.json successfully pushed to s3 bucket",
            "status_code": 200,
        }
    )


@s3_ops.get("/pull-from-s3-bucket")
async def pull_from_s3_bucket(request: Request):
    openapi_json_data = await S3Manager.pull_from_s3_bucket()
    print(openapi_json_data)
    return send_response(
        body={"openapi_json_data": openapi_json_data, "status_code": 200}
    )
