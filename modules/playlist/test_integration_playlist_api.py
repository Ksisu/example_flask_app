import pytest
from flask import Flask

from modules.auth.auth_service import AuthService
from modules.auth.jwt_service import JwtServiceConfig, JwtService
from modules.playlist.playlist_api import create_playlist_blueprint
from modules.playlist.playlist_repository import PlaylistData
from modules.playlist.playlist_repository_inmemory import PlaylistRepositoryInMemory
from modules.playlist.playlist_service import PlaylistService
from modules.test_util.get_test_names import get_test_names

GOOD_JWT = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyb2xlcyI6W10sIm9yZ19pbmZvIjp7Im9yZ19pZCI6WyJvcmdfaWRfMTIzIl19fQ.aMRAPWTlfpwgeKlQNPC8wloZ0kUJne_81FP3Bp2vDas"
ORG_ID = "org_id_123"
GOOD_HEADERS = {
    "Authorization": "Bearer " + GOOD_JWT,
    "X-OrganisationId": ORG_ID,
    "content-type": "application/json",
}
WRONG_HEADERS = {
    "Authorization": "Bearer " + GOOD_JWT,
    "X-OrganisationId": "other_org_id",
    "content-type": "application/json",
}

TEST_PLAYLISTS = list([
    PlaylistData(ORG_ID, "name 1", "description 1", "id_1"),
    PlaylistData(ORG_ID, "name 2", "description 2", "id_2"),
    PlaylistData("other_org", "name 3", "description 3", "id_3"),
])
TEST_PLAYLISTS_JSON_DICT = list([
    {"id": "id_1", "name": "name 1", "description": "description 1", "organisation_id": ORG_ID},
    {"id": "id_2", "name": "name 2", "description": "description 2", "organisation_id": ORG_ID},
    {"id": "id_3", "name": "name 3", "description": "description 3", "organisation_id": "other_org"},
])

test_params = [
    {
        "test_name": "GET /playlist success_empty",
        "init_repo_data": list(),
        "test_call": lambda c: c.get("/playlist", headers=GOOD_HEADERS),
        "expected_status_code": 200,
        "expected_response": [],
    },
    {
        "test_name": "GET /playlist success_response",
        "init_repo_data": TEST_PLAYLISTS,
        "test_call": lambda c: c.get("/playlist", headers=GOOD_HEADERS),
        "expected_status_code": 200,
        "expected_response": [
            TEST_PLAYLISTS_JSON_DICT[0],
            TEST_PLAYLISTS_JSON_DICT[1],
        ],
    },
    {
        "test_name": "GET /playlist failed_auth",
        "init_repo_data": list(),
        "test_call": lambda c: c.get("/playlist", headers=WRONG_HEADERS),
        "expected_status_code": 401,
        "expected_response": {"error_code": 1000, "message": "Not have permission to this organisation"},
    },
    {
        "test_name": "GET /playlist/<playlist_id> success",
        "init_repo_data": TEST_PLAYLISTS,
        "test_call": lambda c: c.get("/playlist/" + TEST_PLAYLISTS[0].id, headers=GOOD_HEADERS),
        "expected_status_code": 200,
        "expected_response": TEST_PLAYLISTS_JSON_DICT[0],
    },
    {
        "test_name": "GET /playlist/<playlist_id> failed_not_found",
        "init_repo_data": list(),
        "test_call": lambda c: c.get("/playlist/" + TEST_PLAYLISTS[0].id, headers=GOOD_HEADERS),
        "expected_status_code": 400,
        "expected_response": {"error_code": 2000, "message": "Playlist not found"},
    },
    {
        "test_name": "GET /playlist/<playlist_id> failed_belongs_to_other_organisation",
        "init_repo_data": TEST_PLAYLISTS,
        "test_call": lambda c: c.get("/playlist/" + TEST_PLAYLISTS[2].id, headers=GOOD_HEADERS),
        "expected_status_code": 400,
        "expected_response": {"error_code": 2000, "message": "Playlist not found"},
    },
    {
        "test_name": "GET /playlist/<playlist_id> failed_auth",
        "init_repo_data": TEST_PLAYLISTS,
        "test_call": lambda c: c.get("/playlist/" + TEST_PLAYLISTS[0].id, headers=WRONG_HEADERS),
        "expected_status_code": 401,
        "expected_response": {"error_code": 1000, "message": "Not have permission to this organisation"},
    },
    {
        "test_name": "POST /playlist success",
        "init_repo_data": list(),
        "test_call": lambda c: c.post("/playlist", data="""{"name":"new playlist"}""", headers=GOOD_HEADERS),
        "expected_status_code": 200,
        "expected_response": {},
    },
    {
        "test_name": "POST /playlist auth_failed",
        "init_repo_data": list(),
        "test_call": lambda c: c.post("/playlist", data="""{"name":"new playlist"}""", headers=WRONG_HEADERS),
        "expected_status_code": 401,
        "expected_response": {"error_code": 1000, "message": "Not have permission to this organisation"},
    },
    {
        "test_name": "DELETE /playlist/<playlist_id> success",
        "init_repo_data": TEST_PLAYLISTS,
        "test_call": lambda c: c.delete("/playlist/" + TEST_PLAYLISTS[0].id, headers=GOOD_HEADERS),
        "expected_status_code": 200,
        "expected_response": {},
    },
    {
        "test_name": "DELETE /playlist/<playlist_id> failed_auth",
        "init_repo_data": TEST_PLAYLISTS,
        "test_call": lambda c: c.delete("/playlist/" + TEST_PLAYLISTS[0].id, headers=WRONG_HEADERS),
        "expected_status_code": 401,
        "expected_response": {"error_code": 1000, "message": "Not have permission to this organisation"},
    },
]


@pytest.mark.parametrize("params", test_params, ids=get_test_names(test_params))
def test_integration_playlist_api(params):
    auth_service = AuthService(JwtService(JwtServiceConfig("HS256", "secret")))
    playlist_repository = PlaylistRepositoryInMemory(params["init_repo_data"])
    playlist_service = PlaylistService(playlist_repository)

    bp = create_playlist_blueprint(auth_service, playlist_service)
    app = Flask(__name__)
    app.register_blueprint(bp)
    app.config["DEBUG"] = True
    app.config["TESTING"] = True
    client = app.test_client()

    response = params["test_call"](client)
    assert response.status_code == params["expected_status_code"]
    assert response.content_type == "application/json"
    assert response.json == params["expected_response"]
