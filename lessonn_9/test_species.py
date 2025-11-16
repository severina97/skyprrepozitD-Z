from sqlalchemy import text
from db import db
from config import (
    TEST_SPECIES_ID,
    TEST_SPECIES_NAME_CREATE,
    TEST_SPECIES_NAME_UPDATE,
)


def test_create_species():
    with db.connect() as connection:
        sql = text("""
            INSERT INTO species (species_id, species_name)
            VALUES (:id, :name)
        """)
        connection.execute(sql, {
            "id": TEST_SPECIES_ID,
            "name": TEST_SPECIES_NAME_CREATE
        })
        connection.commit()


def test_update_species():
    with db.connect() as connection:
        sql = text("""
            UPDATE species
            SET species_name = :name
            WHERE species_id = :id
        """)
        connection.execute(sql, {
            "name": TEST_SPECIES_NAME_UPDATE,
            "id": TEST_SPECIES_ID
        })
        connection.commit()


def test_delete_species():
    with db.connect() as connection:
        sql = text("DELETE FROM species WHERE species_id = :id")
        connection.execute(sql, {"id": TEST_SPECIES_ID})
        connection.commit()
