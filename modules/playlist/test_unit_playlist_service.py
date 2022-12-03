from unittest.mock import MagicMock

from modules.auth.auth_service import AuthData
from modules.common.empty_response import EmptyResponse
from modules.common.error import ApplicationError
from modules.playlist.playlist_repository import PlaylistData, PlaylistRepository
from modules.playlist.playlist_service import PlaylistService, CreatePlaylistData

ORGANISATION_ID_1 = "repository_test_org_777"
PLAYLIST_1 = PlaylistData(id="playlist_1", organisation_id=ORGANISATION_ID_1, name="Playlist name 1",
                          description="Desc1")
PLAYLIST_2 = PlaylistData(id="playlist_2", organisation_id=ORGANISATION_ID_1, name="Playlist name 2",
                          description="Desc2")
PLAYLIST_3 = PlaylistData(id="playlist_3", organisation_id="repository_test_org_888", name="Playlist name 3",
                          description="Desc3")

AUTH_DATA = AuthData(roles=[], organisation_ids=[ORGANISATION_ID_1], current_organisation_id=ORGANISATION_ID_1)


def test_unit_playlist_service_get_playlist_success():
    repo_mock = PlaylistRepository()
    repo_mock.find_playlist = MagicMock(return_value=PLAYLIST_1)
    service = PlaylistService(repo_mock)
    assert service.get_playlist(AUTH_DATA, PLAYLIST_1.id) == PLAYLIST_1
    repo_mock.find_playlist.assert_called_once_with(PLAYLIST_1.id)


def test_unit_playlist_service_get_playlist_fail_not_found():
    repo_mock = PlaylistRepository()
    repo_mock.find_playlist = MagicMock(return_value=None)
    service = PlaylistService(repo_mock)
    assert service.get_playlist(AUTH_DATA, PLAYLIST_1.id) == ApplicationError(2000, "Playlist not found")


def test_unit_playlist_service_get_playlist_fail_belongs_to_other_organisation():
    repo_mock = PlaylistRepository()
    repo_mock.find_playlist = MagicMock(return_value=PLAYLIST_3)
    service = PlaylistService(repo_mock)
    assert service.get_playlist(AUTH_DATA, PLAYLIST_3.id) == ApplicationError(2000, "Playlist not found")


def test_unit_playlist_service_list_organisation_playlists_use_current_organisation():
    repo_mock = PlaylistRepository()
    repo_mock.find_playlist_by_organisation = MagicMock(return_value=list([PLAYLIST_1, PLAYLIST_2]))
    service = PlaylistService(repo_mock)
    assert service.list_organisation_playlists(AUTH_DATA) == list([PLAYLIST_1, PLAYLIST_2])
    repo_mock.find_playlist_by_organisation.assert_called_once_with(AUTH_DATA.current_organisation_id)


def test_unit_playlist_service_create_playlist_success():
    repo_mock = PlaylistRepository()
    repo_mock.add_playlist = MagicMock(return_value=None)
    service = PlaylistService(repo_mock)
    data = CreatePlaylistData(name="Test new playlist")
    assert service.create_playlist(AUTH_DATA, data) == EmptyResponse()
    repo_mock.add_playlist.assert_called_once()
    saved_data = repo_mock.add_playlist.call_args[0][0]
    assert isinstance(saved_data, PlaylistData)
    assert saved_data.name == "Test new playlist"
    assert saved_data.organisation_id == AUTH_DATA.current_organisation_id


def test_unit_playlist_service_delete_playlist_success():
    repo_mock = PlaylistRepository()
    repo_mock.find_playlist = MagicMock(return_value=PLAYLIST_1)
    repo_mock.delete_playlist = MagicMock(return_value=None)
    service = PlaylistService(repo_mock)
    assert service.delete_playlist(AUTH_DATA, PLAYLIST_1.id) == EmptyResponse()
    repo_mock.find_playlist.assert_called_once_with(PLAYLIST_1.id)
    repo_mock.delete_playlist.assert_called_once_with(PLAYLIST_1.id)


def test_unit_playlist_service_delete_playlist_success_not_delete_other_organisations_playlist():
    repo_mock = PlaylistRepository()
    repo_mock.find_playlist = MagicMock(return_value=PLAYLIST_3)
    repo_mock.delete_playlist = MagicMock(return_value=None)
    service = PlaylistService(repo_mock)
    assert service.delete_playlist(AUTH_DATA, PLAYLIST_3.id) == EmptyResponse()
    repo_mock.find_playlist.assert_called_once_with(PLAYLIST_3.id)
    repo_mock.delete_playlist.assert_not_called()


def test_unit_playlist_service_delete_playlist_success_not_found():
    repo_mock = PlaylistRepository()
    repo_mock.find_playlist = MagicMock(return_value=None)
    repo_mock.delete_playlist = MagicMock(return_value=None)
    service = PlaylistService(repo_mock)
    assert service.delete_playlist(AUTH_DATA, PLAYLIST_1.id) == EmptyResponse()
    repo_mock.find_playlist.assert_called_once_with(PLAYLIST_1.id)
    repo_mock.delete_playlist.assert_not_called()
