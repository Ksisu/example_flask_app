from unittest.mock import MagicMock
from flask import Blueprint, Flask

from modules.auth.auth_service import AuthService
from modules.auth.protected_endpoint_decorator import create_protected_endpoint_decorator


def dummy_handler(_auth_service, _request, function, *args, **kwargs):
    # Just pass arguments to the endpoint
    return function(_auth_service, *args, **kwargs)


protected_decorator_test = create_protected_endpoint_decorator(dummy_handler)


def test_create_protected_endpoint_decorator_call_endpoint_and_create_json_response():
    auth_service_mock = AuthService(None)
    bp = Blueprint("testbp", __name__)
    mock_endpoint = MagicMock(return_value=( {"random": "response"}, 456))
    protected_decorator_test(auth_service_mock, bp, "/test/<parameter>/<other_param>", methods=["GET"])(mock_endpoint)

    app = Flask(__name__)
    app.register_blueprint(bp)
    app.config["DEBUG"] = True
    app.config["TESTING"] = True
    client = app.test_client()

    response = client.get("/test/random_parameter/other")
    assert response.status_code == 456
    assert response.content_type == "application/json"
    assert response.json == {"random": "response"}
    mock_endpoint.assert_called_once()
    called_args = mock_endpoint.call_args_list[0]
    assert called_args.args[0] == auth_service_mock
    assert called_args.kwargs == {"parameter": "random_parameter", "other_param": "other"}


def test_create_protected_endpoint_decorator_handle_multiple_path_with_same_name():
    bp = Blueprint("testbp", __name__)
    protected_decorator_test(None, bp, "/test/<parameter>/<other_param>", methods=["POST"])(None)
    protected_decorator_test(None, bp, "/test/<parameter>/<other_param>", methods=["GET"])(None)

    app = Flask(__name__)
    app.register_blueprint(bp)
    endpoints = list(app.view_functions.keys())

    assert len(endpoints) == 3
    assert endpoints[0] == "static"
    endpoint_name_post = endpoints[1]
    endpoint_name_get = endpoints[2]
    assert endpoint_name_post.startswith("testbp./test/<parameter>/<other_param>_")
    assert endpoint_name_get.startswith("testbp./test/<parameter>/<other_param>_")
    assert endpoint_name_get != endpoint_name_post
