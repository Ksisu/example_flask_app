import pytest

from src.modules.auth.jwt_service import JwtServiceConfig, JwtService
from tests.test_util.get_test_names import get_test_names

test_params = [
    {
        "test_name": "success",
        "jwt": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyYW5kb20iOiJkYXRhIiwiZXhwIjoyMzk1ODIxMDU2fQ.CfajFIT_29nZ_QUKlYGmq8_mu0C_1_p5GcGKU854Dcw",
        "expected": {"random": "data", "exp": 2395821056},
    },
    {
        "test_name": "failed_wrong_secret",
        "jwt": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyYW5kb20iOiJkYXRhIiwiZXhwIjoyMzk1ODIxMDU2fQ.PN6Gc2Nc3TgPIez3Qp31IOVG_9oRlsORWzEslg-yEWQ",
        "expected": None,
    },
    {
        "test_name": "failed_expired",
        "jwt": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyYW5kb20iOiJkYXRhIiwiZXhwIjoxMDAwMDAwfQ.AucGmFPXvkfjTSwz5yir2RD2JHpntLiTda1JgwNFq30",
        "expected": None,
    }
]


@pytest.mark.parametrize("data", test_params, ids=get_test_names(test_params))
def test_unit_jwt_service(data):
    jwt_service = JwtService(JwtServiceConfig("HS256", "secret_1"))
    assert jwt_service.decode(data["jwt"]) == data["expected"]
