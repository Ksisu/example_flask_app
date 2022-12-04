import pytest

from src.modules.auth.auth_service import AuthData
from tests.test_util.get_test_names import get_test_names

ORGANISATION_ID_1 = "repository_test_org_777"
ORGANISATION_ID_2 = "repository_test_org_888"
ADMIN_ROLE = "ci_super_admin"

test_params = [
    {
        "test_name": "empty",
        "auth_data": AuthData(roles=list(), organisation_ids=list()),
        "expected_is_admin": False,
        "expected_has_access_org1": False,
        "expected_has_access_org2": False,
    },
    {
        "test_name": "dummy_role",
        "auth_data": AuthData(roles=list("dummy_role"), organisation_ids=list()),
        "expected_is_admin": False,
        "expected_has_access_org1": False,
        "expected_has_access_org2": False,
    },
    {
        "test_name": "admin_role",
        "auth_data": AuthData(roles=list([ADMIN_ROLE]), organisation_ids=list()),
        "expected_is_admin": True,
        "expected_has_access_org1": True,
        "expected_has_access_org2": True,
    },
    {
        "test_name": "access_org1_no_admin",
        "auth_data": AuthData(roles=list(), organisation_ids=list([ORGANISATION_ID_1])),
        "expected_is_admin": False,
        "expected_has_access_org1": True,
        "expected_has_access_org2": False,
    },
    {
        "test_name": "access_org12_no_admin",
        "auth_data": AuthData(roles=list(), organisation_ids=list([ORGANISATION_ID_1, ORGANISATION_ID_2])),
        "expected_is_admin": False,
        "expected_has_access_org1": True,
        "expected_has_access_org2": True,
    },
]


@pytest.mark.parametrize("data", test_params, ids=get_test_names(test_params))
def test_unit_auth_data(data):
    auth_data = data["auth_data"]
    assert auth_data.is_admin() == data["expected_is_admin"]
    assert auth_data.has_permission_to_organisation(ORGANISATION_ID_1) == data["expected_has_access_org1"]
    assert auth_data.has_permission_to_organisation(ORGANISATION_ID_2) == data["expected_has_access_org2"]
