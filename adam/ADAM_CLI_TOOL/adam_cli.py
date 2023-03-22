import json
import typer
import ujson
import aiohttp
import asyncio
from typing import Optional
from openapi_spec_validator import openapi_v30_spec_validator,validate_spec
from openapi_spec_validator.validation.exceptions import *
from swagger_spec_validator.validator12 import validate_resource_listing

"""

VALIDATION METHODS

Two methods can be used to validate 'openapi.json file'


1 . SWAGGER-CODEGEN :- It is a code generation tool which can be used for validation also. We have to 
                       install it into our local machine and then run the validation command with the
                       syntax 'swagger-codegen validate -i openapi.json'

2. OpenAPI 3.0 Validator:- It is a python library that validates OpenAPI 3.0 files against the openapi
                           specification. We have to install it using 'pip install openapi-core' and then
                           use it to validate our file.
                           
"""


def get_openapi_file(_path: str) -> dict:
    with open(_path) as openapi_file:
        openapi = ujson.load(openapi_file)
    return openapi


def get_and_validate_openapi_file(path: Optional[str] = "./openapi.json"):
    """
    This function renders the openapi.json and also validates it
    After validation the file is pushed to S3 Bucket

    : param path: Type: Optional
                  default: './openapi.json'
                  description: Path of OpenAPI Specification file including name
    : return: JSON response
    """
    openapi_file = None
    try:
        openapi_file = get_openapi_file(path)
        validate_spec(spec=openapi_file, validator=openapi_v30_spec_validator)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        _response = loop.run_until_complete(
            push_openapi_file_to_s3_bucket(openapi_file)
        )
        loop.close()
        typer.echo("File successfully pushed to S3 Bucket")
        return 0
    except (
        TypeError,
        FileNotFoundError,
        ValueError,
        json.JSONDecodeError,
        OpenAPIValidationError,
        ValidatorDetectError,
        ExtraParametersError,
        ParameterDuplicateError,
        UnresolvableParameterError,
        DuplicateOperationIDError,
    ) as exception:
        return handle_exception(exception)


def handle_exception(exception):
    print(exception.__class__.__name__, str(exception))
    return 1


async def push_openapi_file_to_s3_bucket(openapi_json_file):
    """
    This function calls the ADAM endpoint and
    pushes the 'openapi.json' file to S3 Bucket.
    """
    async with aiohttp.ClientSession() as session:
        async with session.post(
            "http://0.0.0.0:8090/v4/push-to-s3-bucket", json=openapi_json_file
        ) as response:
            _response = await response.json()
    return _response


if __name__ == "__main__":
    typer.run(get_and_validate_openapi_file)
