from unittest.mock import MagicMock

import dataclasses_jsonschema
import flask

from modules.auth.auth_service import AuthService, AuthData, AuthError
from modules.common.error import ApplicationError
from modules.auth.protected_endpoint_decorator import protected_endpoint_handler

SUCCESS_AUTH_DATA_MOCK = AuthData(list(["role1"]), list(["current_org"]), "current_org")
REQUEST = flask.Request.from_values()


def test_protected_endpoint_handler_success_pass_auth_data():
    auth_service_mock = AuthService(None)
    auth_service_mock.authenticate = MagicMock(return_value=SUCCESS_AUTH_DATA_MOCK)
    mock_result = {"Some": "response"}
    endpoint_function_mock = MagicMock(return_value=mock_result)
    result = protected_endpoint_handler(auth_service_mock, REQUEST, endpoint_function_mock)
    assert result == (mock_result, 200)
    endpoint_function_mock.assert_called_once_with(SUCCESS_AUTH_DATA_MOCK)
    auth_service_mock.authenticate.assert_called_once_with(REQUEST)

def test_protected_endpoint_handler_success_pass_extra_arguments():
    auth_service_mock = AuthService(None)
    auth_service_mock.authenticate = MagicMock(return_value=SUCCESS_AUTH_DATA_MOCK)
    mock_result = {"Some": "response"}
    endpoint_function_mock = MagicMock(return_value=mock_result)
    result = protected_endpoint_handler(auth_service_mock, REQUEST, endpoint_function_mock, "plus", "random", "args", 123)
    assert result == (mock_result, 200)
    endpoint_function_mock.assert_called_once_with(SUCCESS_AUTH_DATA_MOCK, "plus", "random", "args", 123)
    auth_service_mock.authenticate.assert_called_once_with(REQUEST)


def test_protected_endpoint_handler_application_error():
    auth_service_mock = AuthService(None)
    auth_service_mock.authenticate = MagicMock(return_value=SUCCESS_AUTH_DATA_MOCK)
    mock_result = ApplicationError(123, "Some error")
    endpoint_function_mock = MagicMock(return_value=mock_result)
    result = protected_endpoint_handler(auth_service_mock, REQUEST, endpoint_function_mock)
    assert result == (mock_result, 400)


def test_protected_endpoint_handler_auth_error():
    auth_data_mock = AuthError(123, "Some error")
    auth_service_mock = AuthService(None)
    auth_service_mock.authenticate = MagicMock(return_value=auth_data_mock)
    endpoint_function_mock = MagicMock()
    result = protected_endpoint_handler(auth_service_mock, REQUEST, endpoint_function_mock)
    assert result == (auth_data_mock, 401)
    endpoint_function_mock.assert_not_called()


def test_protected_endpoint_handler_input_schema_validation_error():
    def endpoint_function_mock(_auth_data):
        raise dataclasses_jsonschema.ValidationError()
    auth_service_mock = AuthService(None)
    auth_service_mock.authenticate = MagicMock(return_value=SUCCESS_AUTH_DATA_MOCK)

    result = protected_endpoint_handler(auth_service_mock, REQUEST, endpoint_function_mock)
    assert result == (ApplicationError(9999, "Invalid input data"), 400)
