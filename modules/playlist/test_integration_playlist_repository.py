import random
from dataclasses import replace

import pytest

from modules.database.database_service import DatabaseService, DatabaseServiceConfig
from modules.playlist.playlist_repository import PlaylistData, PlaylistRepository
from modules.playlist.playlist_repository_inmemory import PlaylistRepositoryInMemory
from modules.playlist.playlist_repository_real import PlaylistRepositoryReal

playlist_repository_inmemory = PlaylistRepositoryInMemory()

db_config = DatabaseServiceConfig(host="localhost", port="5555", user="postgres", password="postgres",
                                  database="postgres")
db_service = DatabaseService(db_config)
playlist_repository_real = PlaylistRepositoryReal(db_service)

test_names = [
    "PlaylistRepositoryInMemory",
    "PlaylistRepositoryReal"
]
test_data = [
    playlist_repository_inmemory,
    playlist_repository_real,
]


@pytest.mark.parametrize("repo", test_data, ids=test_names)
def test_unit_playlist_repository_story(repo: PlaylistRepository):
    ORGANISATION_ID = "repository_test_org_" + str(random.randint(0, 100000))
    ORGANISATION_ID_2 = "repository_test_org_" + str(random.randint(0, 100000))
    PLAYLIST_1 = PlaylistData(organisation_id=ORGANISATION_ID, name="Playlist name 1", description="Desc1")
    PLAYLIST_2 = PlaylistData(organisation_id=ORGANISATION_ID, name="Playlist name 2", description="Desc2")
    PLAYLIST_3 = PlaylistData(organisation_id=ORGANISATION_ID_2, name="Playlist name 3", description="Desc3")

    assert repo.find_playlist_by_organisation(ORGANISATION_ID) == list()
    assert repo.find_playlist_by_organisation(ORGANISATION_ID_2) == list()

    repo.add_playlist(PLAYLIST_1)
    repo.add_playlist(PLAYLIST_2)
    repo.add_playlist(PLAYLIST_3)

    org_1_playlists = repo.find_playlist_by_organisation(ORGANISATION_ID)
    assert len(org_1_playlists) == 2
    playlist_id_1 = org_1_playlists[0].id
    playlist_id_2 = org_1_playlists[1].id
    assert org_1_playlists[0] == replace(PLAYLIST_1, id=playlist_id_1)
    assert org_1_playlists[1] == replace(PLAYLIST_2, id=playlist_id_2)

    org_2_playlists = repo.find_playlist_by_organisation(ORGANISATION_ID_2)
    assert len(org_2_playlists) == 1
    playlist_id_3 = org_2_playlists[0].id
    assert org_2_playlists[0] == replace(PLAYLIST_3, id=playlist_id_3)

    playlist = repo.find_playlist(playlist_id_1)
    assert playlist == replace(PLAYLIST_1, id=playlist_id_1)

    repo.delete_playlist(playlist_id_1)

    assert repo.find_playlist(playlist_id_1) is None

    org_1_playlists = repo.find_playlist_by_organisation(ORGANISATION_ID)
    assert len(org_1_playlists) == 1
    assert org_1_playlists[0] == replace(PLAYLIST_2, id=playlist_id_2)
