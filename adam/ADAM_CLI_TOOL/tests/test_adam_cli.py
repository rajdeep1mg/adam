import pytest
import ujson
from openapi_spec_validator.validation.exceptions import OpenAPIValidationError
import ADAM_CLI_TOOL.adam_cli as adam_cli


@pytest.fixture
def openapi():
    _path = "./openapi.json"
    with open(_path) as file:
        openapi = ujson.load(file)
    return openapi


def mock_handle_exceptions(exception):
    return exception.__class__.__name__


@pytest.mark.cli_success
def test_success_cli():
    _path = "./openapi.json"
    cli_success_correct_response = 0
    assert adam_cli.get_and_validate_openapi_file(_path) == cli_success_correct_response


@pytest.mark.cli_failure
def test_file_not_found_exception(monkeypatch):
    _path = "invalid_openapi.json"
    test_file_not_found_correct_response = 1
    monkeypatch.setattr(
        "ADAM_CLI_TOOL.adam_cli.handle_exception", mock_handle_exceptions
    )
    assert adam_cli.get_and_validate_openapi_file(_path) == FileNotFoundError.__name__
    monkeypatch.undo()
    assert (
        adam_cli.get_and_validate_openapi_file(_path)
        == test_file_not_found_correct_response
    )


@pytest.mark.cli_failure
def test_openapi_validation_error(monkeypatch):
    path = "./openapi.json"
    test_openapi_validation_error_correct_response = 1

    def get_file(_path):
        with open(_path) as file:
            openapi = ujson.load(file)
        return openapi

    def mock_get_openapi_file_invalid_value(_path):
        openapi = get_file(_path)
        openapi["info"]["title"] = 1
        return openapi

    def mock_get_openapi_file_attr_not_present(_path):
        openapi = get_file(_path)
        openapi["info"]["version"] = None
        openapi["info"]["title"] = None
        openapi["paths"] = None
        return openapi

    def mock_get_openapi_file_not_correct_type(_path):
        openapi = get_file(_path)
        openapi["info"]["version"] = ["1.0.0"]
        return openapi

    monkeypatch.setattr(
        "ADAM_CLI_TOOL.adam_cli.get_openapi_file", mock_get_openapi_file_invalid_value
    )
    monkeypatch.setattr(
        "ADAM_CLI_TOOL.adam_cli.handle_exception", mock_handle_exceptions
    )
    assert (
        adam_cli.get_and_validate_openapi_file(path) == OpenAPIValidationError.__name__
    )
    monkeypatch.undo()
    monkeypatch.setattr(
        "ADAM_CLI_TOOL.adam_cli.get_openapi_file", mock_get_openapi_file_invalid_value
    )
    assert (
        adam_cli.get_and_validate_openapi_file(path)
        == test_openapi_validation_error_correct_response
    )
    monkeypatch.undo()
    monkeypatch.setattr(
        "ADAM_CLI_TOOL.adam_cli.get_openapi_file",
        mock_get_openapi_file_attr_not_present,
    )
    monkeypatch.setattr(
        "ADAM_CLI_TOOL.adam_cli.handle_exception", mock_handle_exceptions
    )
    assert (
        adam_cli.get_and_validate_openapi_file(path) == OpenAPIValidationError.__name__
    )
    monkeypatch.undo()
    monkeypatch.setattr(
        "ADAM_CLI_TOOL.adam_cli.get_openapi_file", mock_get_openapi_file_invalid_value
    )
    assert (
        adam_cli.get_and_validate_openapi_file(path)
        == test_openapi_validation_error_correct_response
    )
    monkeypatch.undo()
    monkeypatch.setattr(
        "ADAM_CLI_TOOL.adam_cli.get_openapi_file",
        mock_get_openapi_file_not_correct_type,
    )
    monkeypatch.setattr(
        "ADAM_CLI_TOOL.adam_cli.handle_exception", mock_handle_exceptions
    )
    assert (
        adam_cli.get_and_validate_openapi_file(path) == OpenAPIValidationError.__name__
    )
    monkeypatch.undo()
    monkeypatch.setattr(
        "ADAM_CLI_TOOL.adam_cli.get_openapi_file",
        mock_get_openapi_file_not_correct_type,
    )
    assert (
        adam_cli.get_and_validate_openapi_file(path)
        == test_openapi_validation_error_correct_response
    )

