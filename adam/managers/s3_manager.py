import boto3
from torpedo import CONFIG
import json

config = CONFIG.config


class S3Manager:
    @classmethod
    async def push_to_s3_bucket(self, data):
        bucket_name = config["PROJECT_ADAM"]["S3_BUCKET"]["BUCKET_NAME"]
        object_key = config["PROJECT_ADAM"]["S3_BUCKET"]["OBJECT_KEY"]

        s3_client = boto3.client("s3")
        response = s3_client.put_object(Body=data, Bucket=bucket_name, Key=object_key)
        return response

    @classmethod
    async def pull_from_s3_bucket(cls):
        s3 = boto3.resource("s3")
        bucket_name = config["PROJECT_ADAM"]["S3_BUCKET"]["BUCKET_NAME"]
        object_key = config["PROJECT_ADAM"]["S3_BUCKET"]["OBJECT_KEY"]

        s3_object = s3.Object(bucket_name, object_key)
        data = s3_object.get()["Body"].read().decode("utf-8")
        json_data = json.loads(data)
        return json_data
