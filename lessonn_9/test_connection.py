from sqlalchemy import inspect
from db import db


def test_db_connection():
    inspector = inspect(db)
    tables = inspector.get_table_names()

    assert 'company' in tables
    assert 'species' in tables
    assert 'persons' in tables
