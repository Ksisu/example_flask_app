import uuid
from dataclasses import replace

from sqlalchemy import Table, Column, String, MetaData, select, delete

from modules.auth.auth_service import OrganisationId
from modules.database.database_service import DatabaseService
from modules.playlist.playlist_repository import PlaylistData, PlaylistRepository, PlaylistId


class PlaylistRepositoryReal(PlaylistRepository):

    def __init__(self, database_service: DatabaseService):
        self._db = database_service
        self._meta = MetaData()
        self._table = self._create_table(self._meta)

    def _create_table(self, meta: MetaData) -> Table:
        return Table(
            'playlist', meta,
            Column('id', String, primary_key=True),
            Column('name', String),
            Column('description', String),
            Column('organisation_id', String),
        )

    def add_playlist(self, data: PlaylistData) -> None:
        playlist = replace(data, id=str(uuid.uuid4()))
        query = self._table.insert().values(**playlist.__dict__)
        self._db.execute(query)

    def delete_playlist(self, playlist_id: PlaylistId) -> None:
        t = self._table
        query = delete(t).where(t.c.id == playlist_id)
        self._db.execute(query)

    def find_playlist(self, playlist_id: PlaylistId) -> PlaylistData | None:
        t = self._table
        query = select(t).where(t.c.id == playlist_id)
        result = self._db.execute(query)
        if result.rowcount == 0:
            return None
        return PlaylistData(**result.fetchone())

    def find_playlist_by_organisation(self, organisation_id: OrganisationId) -> list[PlaylistData]:
        t = self._table
        query = select(t).where(t.c.organisation_id == organisation_id)
        result = self._db.execute(query)
        return list(map(lambda r: PlaylistData(**r), result.fetchall()))
