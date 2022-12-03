from dataclasses import dataclass, replace
from typing import TypeAlias

import flask

from modules.auth.jwt_service import JwtService
from modules.common.error import ApplicationError

OrganisationId: TypeAlias = str


@dataclass
class AuthData:
    roles: list[str]
    organisation_ids: list[OrganisationId]
    current_organisation_id: str = None

    # TODO add user info

    def is_admin(self):
        return "ci_super_admin" in self.roles

    def has_permission_to_organisation(self, organisation_id):
        return self.is_admin() or organisation_id in self.organisation_ids


@dataclass
class AuthError(ApplicationError):
    pass


class AuthService:
    def __init__(self, jwt_service: JwtService):
        self._jwt_service = jwt_service

    def authenticate(self, request: flask.Request) -> AuthError | AuthData:
        organisation_id = self._get_organisation_id(request)
        if isinstance(organisation_id, AuthError):
            return organisation_id

        jwt = self._get_jwt(request)
        if isinstance(jwt, AuthError):
            return jwt

        auth_data = self._parse_and_validate_jwt(jwt)
        if isinstance(auth_data, AuthError):
            return auth_data

        if not auth_data.has_permission_to_organisation(organisation_id):
            return AuthError(1000, "Not have permission to this organisation")

        return replace(auth_data, current_organisation_id=organisation_id)

    def _get_jwt(self, request: flask.Request) -> AuthError | str:
        auth_header = request.headers.get("Authorization")
        if auth_header is None:
            return AuthError(1001, "Missing authorization header")
        return auth_header.removeprefix("Bearer ")

    def _parse_and_validate_jwt(self, raw_jwt: str) -> AuthError | AuthData:
        jwt = self._jwt_service.decode(raw_jwt)
        if jwt is None:
            return AuthError(1002, "Invalid JWT")

        roles = jwt["roles"]
        if "org_info" not in jwt or "org_id" not in jwt["org_info"]:
            organisation_ids = []
        else:
            organisation_ids = jwt["org_info"]["org_id"]
        return AuthData(roles, organisation_ids)

    def _get_organisation_id(self, request: flask.Request) -> AuthError | OrganisationId:
        org_id = request.headers.get('X-OrganisationId')
        if org_id is not None:
            return org_id
        return AuthError(1003, "Missing X-OrganisationId header")
