import pytest

from src.modules.database.database_service import DatabaseServiceConfig, DatabaseService


def test_integration_database_service_success():
    db_config = DatabaseServiceConfig(host="localhost", port="5555", user="postgres", password="postgres",
                                      database="postgres")
    db_service = DatabaseService(db_config)
    assert db_service.test_connection() is None


def test_integration_database_service_fail():
    db_config = DatabaseServiceConfig(host="wrong", port="000", user="wrong", password="wrong",
                                      database="wrong")
    db_service = DatabaseService(db_config)
    with pytest.raises(Exception):
        db_service.test_connection()
