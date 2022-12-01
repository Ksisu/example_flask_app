from flask import Flask

from modules.auth.auth_service import AuthService
from modules.auth.jwt_service import JwtServiceConfig, JwtService
from modules.playlist.playlist_api import create_playlist_blueprint
from modules.playlist.playlist_repository import PlaylistRepository
from modules.playlist.playlist_service import PlaylistService


def init(main_app: Flask):
    # jwt_config = JwtServiceConfig.read_from_env()
    jwt_config = JwtServiceConfig("HS256", "secret")
    jwt_service = JwtService(jwt_config)
    auth_service = AuthService(jwt_service)

    playlist_repository = PlaylistRepository()
    playlist_service = PlaylistService(playlist_repository)
    playlist_blueprint = create_playlist_blueprint(auth_service, playlist_service)
    main_app.register_blueprint(playlist_blueprint)


app = Flask(__name__)
init(app)


if __name__ == '__main__':
    app.run()
