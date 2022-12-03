import random

import dataclasses_jsonschema
import flask
from flask import request, jsonify, make_response, Blueprint

from modules.auth.auth_service import AuthService, AuthError
from modules.common.error import ApplicationError


def create_protected_endpoint_decorator(endpoint_handler):
    def _protected_endpoint(auth_service: AuthService, bp: Blueprint, path: str, *args, **kwargs):
        def decorator(function):
            def wrapper(*args_, **kwargs_):
                body, status_code = endpoint_handler(auth_service, request, function, *args_, **kwargs_)
                return make_response(jsonify(body), status_code)

            endpoint = path + "_" + str(random.randint(0, 10000))
            bp.add_url_rule(path, endpoint, wrapper, *args, **kwargs)
            return wrapper

        return decorator

    return _protected_endpoint


def protected_endpoint_handler(auth_service: AuthService, req: flask.Request, endpoint_function, *args, **kwargs):
    try:
        auth_data = auth_service.authenticate(req)
        if isinstance(auth_data, AuthError):
            return auth_data, 401
        result = endpoint_function(auth_data, *args, **kwargs)
        if isinstance(result, ApplicationError):
            return result, 400
        return result, 200
    except dataclasses_jsonschema.ValidationError:
        return ApplicationError(9999, "Invalid input data"), 400


protected_endpoint = create_protected_endpoint_decorator(protected_endpoint_handler)
