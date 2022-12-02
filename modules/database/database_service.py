import os
from dataclasses import dataclass

from sqlalchemy import create_engine


@dataclass
class DatabaseServiceConfig:
    host: str
    port: str
    user: str
    password: str
    database: str

    def get_connection_url(self) -> str:
        return "postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}".format(**self.__dict__)

    @staticmethod
    def read_from_env():
        host = os.getenv("DB_HOST")
        port = os.getenv("DB_PORT")
        user = os.getenv("DB_USER")
        password = os.getenv("DB_PASSWORD")
        database = os.getenv("DB_DATABASE")
        return DatabaseServiceConfig(host, port, user, password, database)


class DatabaseService:
    def __init__(self, config: DatabaseServiceConfig):
        self._config = config
        self._engine = create_engine(self._config.get_connection_url())

    def execute(self, query: str):
        with self._engine.connect() as con:
            return con.execute(query)

    def test_connection(self):
        assert self.execute("select 1").rowcount == 1
