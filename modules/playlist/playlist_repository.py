from dataclasses import dataclass, replace
import uuid

from modules.auth.auth_service import OrganisationId
from typing import TypeAlias

PlaylistId: TypeAlias = str


@dataclass
class PlaylistData:
    organisation_id: OrganisationId
    name: str
    description: str = ""
    id: PlaylistId = ""


# Dummy repository... should use real db
class PlaylistRepository:
    _playlists: list[PlaylistData] = list()

    def add_playlist(self, data: PlaylistData) -> None:
        id = str(uuid.uuid4())
        playlist = replace(data, id=id)
        self._playlists.append(playlist)  # ugly.. should be immutable

    def delete_playlist(self, playlist_id: PlaylistId) -> None:
        self._playlists = list(filter(lambda p: p.id != playlist_id, self._playlists))

    def get_playlist(self, playlist_id) -> PlaylistData | None:
        return next((p for p in self._playlists if p.id == playlist_id), None)

    def find_playlist_biy_organisation(self, organisation_id: OrganisationId) -> list[PlaylistData]:
        return list(filter(lambda p: p.organisation_id == organisation_id, self._playlists))
