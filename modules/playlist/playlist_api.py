from flask import Blueprint, request

from modules.auth.auth_service import AuthService, AuthData
from modules.auth.protected_endpoint_decorator import protected_endpoint
from modules.playlist.playlist_repository_inmemory import PlaylistId
from modules.playlist.playlist_service import PlaylistService, CreatePlaylistData


def create_playlist_blueprint(auth_service: AuthService, playlist_service: PlaylistService) -> Blueprint:
    bp = Blueprint('playlist', __name__)

    @protected_endpoint(auth_service, bp, "/playlist")
    def list_playlists(auth_data: AuthData):
        return playlist_service.list_organisation_playlists(auth_data)

    @protected_endpoint(auth_service, bp, "/playlist/<playlist_id>")
    def get_playlist(auth_data: AuthData, playlist_id: PlaylistId):
        return playlist_service.get_playlist(auth_data, playlist_id)

    @protected_endpoint(auth_service, bp, "/playlist", methods=["POST"])
    def add_playlist(auth_data: AuthData):
        create_data = CreatePlaylistData.from_dict(request.json)
        return playlist_service.create_playlist(auth_data, create_data)

    @protected_endpoint(auth_service, bp, "/playlist/<playlist_id>", methods=["DELETE"])
    def delete_playlist(auth_data: AuthData, playlist_id: PlaylistId):
        return playlist_service.delete_playlist(auth_data, playlist_id)

    return bp
