from abc import abstractmethod
from dataclasses import dataclass
from typing import TypeAlias

from src.modules.auth.auth_service import OrganisationId

PlaylistId: TypeAlias = str


@dataclass
class PlaylistData:
    organisation_id: OrganisationId
    name: str
    description: str = ""
    id: PlaylistId = ""


class PlaylistRepository:
    @abstractmethod
    def add_playlist(self, data: PlaylistData) -> None:
        pass

    @abstractmethod
    def delete_playlist(self, playlist_id: PlaylistId) -> None:
        pass

    @abstractmethod
    def find_playlist(self, playlist_id: PlaylistId) -> PlaylistData | None:
        pass

    @abstractmethod
    def find_playlist_by_organisation(self, organisation_id: OrganisationId) -> list[PlaylistData]:
        pass
