from dataclasses import dataclass

from modules.auth.auth_service import AuthData
from modules.common.empty_response import EmptyResponse
from modules.common.error import ApplicationError
from modules.playlist.playlist_repository import PlaylistRepository, PlaylistData, PlaylistId

from dataclasses_jsonschema import JsonSchemaMixin


@dataclass
class CreatePlaylistData(JsonSchemaMixin):
    """Creating playlist data"""
    name: str


class PlaylistService:
    def __init__(self, playlist_repository: PlaylistRepository):
        self._playlist_repository = playlist_repository

    def create_playlist(self, auth_data: AuthData, create_data: CreatePlaylistData) -> EmptyResponse:
        data = PlaylistData(name=create_data.name, organisation_id=auth_data.current_organisation_id)
        self._playlist_repository.add_playlist(data)
        return EmptyResponse()

    def delete_playlist(self, auth_data: AuthData, playlist_id: PlaylistId) -> EmptyResponse:
        playlist = self._playlist_repository.get_playlist(playlist_id)
        if playlist is None or not auth_data.has_permission_to_organisation(playlist.organisation_id):
            return EmptyResponse()
        self._playlist_repository.delete_playlist(playlist_id)
        return EmptyResponse()

    def get_playlist(self, auth_data: AuthData, playlist_id: PlaylistId) -> ApplicationError | PlaylistData:
        playlist = self._playlist_repository.get_playlist(playlist_id)
        if playlist is None or not auth_data.has_permission_to_organisation(playlist.organisation_id):
            return ApplicationError(2000, "Playlist not found")
        return playlist

    def list_organisation_playlists(self, auth_data: AuthData) -> list[PlaylistData]:
        playlists = self._playlist_repository.find_playlist_biy_organisation(auth_data.current_organisation_id)
        return playlists
