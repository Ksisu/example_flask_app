import uuid
from dataclasses import replace

from modules.auth.auth_service import OrganisationId
from modules.playlist.playlist_repository import PlaylistData, PlaylistRepository, PlaylistId


# Dummy repository for testing
class PlaylistRepositoryInMemory(PlaylistRepository):
    def __init__(self, initdata=None):
        if initdata is None:
            initdata = list()
        self._playlists = initdata

    def add_playlist(self, data: PlaylistData) -> None:
        id = str(uuid.uuid4())
        playlist = replace(data, id=id)
        self._playlists.append(playlist)  # ugly.. should be immutable

    def delete_playlist(self, playlist_id: PlaylistId) -> None:
        self._playlists = list(filter(lambda p: p.id != playlist_id, self._playlists))

    def find_playlist(self, playlist_id: PlaylistId) -> PlaylistData | None:
        return next((p for p in self._playlists if p.id == playlist_id), None)

    def find_playlist_by_organisation(self, organisation_id: OrganisationId) -> list[PlaylistData]:
        return list(filter(lambda p: p.organisation_id == organisation_id, self._playlists))
