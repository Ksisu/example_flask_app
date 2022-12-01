import dataclasses_jsonschema
import flask
from flask import request, jsonify, make_response, Blueprint
import random

from modules.auth.auth_service import AuthService, AuthError
from modules.common.error import ApplicationError


def protected_endpoint(auth_service: AuthService, bp: Blueprint, path: str, *args, **kwargs):
    def decorator(function):
        def wrapper(*args_, **kwargs_):
            return _protected_endpoint(auth_service, request, function, *args_, **kwargs_)
        endpoint = path + "_" + str(random.randint(0, 10000))
        bp.add_url_rule(path, endpoint, wrapper, *args, **kwargs)
        return wrapper
    return decorator


def _protected_endpoint(auth_service: AuthService, req: flask.Request, endpoint_function, *args, **kwargs):
    try:
        auth_data = auth_service.authenticate(req)
        if isinstance(auth_data, AuthError):
            return make_response(jsonify(auth_data), 401)
        result = endpoint_function(auth_data, *args, **kwargs)
        if isinstance(result, ApplicationError):
            return make_response(jsonify(result), 400)
        return make_response(jsonify(result), 200)
    except dataclasses_jsonschema.ValidationError:
        return make_response(jsonify(ApplicationError(9999, "Invalid input data")), 200)