from unittest.mock import MagicMock

import flask

from modules.auth.auth_service import AuthData, AuthError, AuthService
from modules.auth.jwt_service import JwtServiceConfig, JwtService

ROLES = list(["random_role"])
ORGANISATION_IDS = list(["org_1", "org2"])
DUMMY_JWT = "DUMMY_JWT"
MOCK_JWT_PAYLOAD = {"roles": ROLES, "org_info": {"org_id": ORGANISATION_IDS}}

JWT_SERVICE_MOCK = JwtService(JwtServiceConfig("", ""))
JWT_SERVICE_MOCK.decode = MagicMock(return_value=MOCK_JWT_PAYLOAD)
SERVICE = AuthService(JWT_SERVICE_MOCK)


def test_unit_auth_service_authenticate_success():
    JWT_SERVICE_MOCK.decode.reset_mock()
    request = flask.Request.from_values(headers={
        "Authorization": "Bearer " + DUMMY_JWT,
        "X-OrganisationId": ORGANISATION_IDS[0],
    })
    result = SERVICE.authenticate(request)
    assert isinstance(result, AuthData)
    assert result == AuthData(ROLES, ORGANISATION_IDS, current_organisation_id=ORGANISATION_IDS[0])
    JWT_SERVICE_MOCK.decode.assert_called_once_with(DUMMY_JWT)


def test_unit_auth_service_authenticate_failed_not_have_access():
    JWT_SERVICE_MOCK.decode.reset_mock()
    request = flask.Request.from_values(headers={
        "Authorization": "Bearer " + DUMMY_JWT,
        "X-OrganisationId": "other_org",
    })
    result = SERVICE.authenticate(request)
    assert isinstance(result, AuthError)
    assert result == AuthError(1000, "Not have permission to this organisation")
    JWT_SERVICE_MOCK.decode.assert_called_once_with(DUMMY_JWT)


def test_unit_auth_service_authenticate_failed_missing_auth_header():
    JWT_SERVICE_MOCK.decode.reset_mock()
    request = flask.Request.from_values(headers={
        "X-OrganisationId": "other_org",
    })
    result = SERVICE.authenticate(request)
    assert isinstance(result, AuthError)
    assert result == AuthError(1001, "Missing authorization header")
    JWT_SERVICE_MOCK.decode.assert_not_called()


def test_unit_auth_service_authenticate_failed_missing_organisation():
    JWT_SERVICE_MOCK.decode.reset_mock()
    request = flask.Request.from_values(headers={
        "Authorization": "Bearer " + DUMMY_JWT,
    })
    result = SERVICE.authenticate(request)
    assert isinstance(result, AuthError)
    assert result == AuthError(1003, "Missing X-OrganisationId header")
