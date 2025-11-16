from sqlalchemy import text
from db import db
from config import TEST_COMPANY_ID, TEST_COMPANY_NAME


def test_select_company_first_row():
    with db.connect() as connection:
        result = connection.execute(text("SELECT * FROM company"))
        rows = result.mappings().all()
        row1 = rows[0]
        assert row1["id"] == TEST_COMPANY_ID
        assert row1["name"] == TEST_COMPANY_NAME


def test_select_one_company():
    with db.connect() as connection:
        sql = text("SELECT * FROM company WHERE id = :id")
        result = connection.execute(sql, {"id": TEST_COMPANY_ID})
        rows = result.mappings().all()

        assert len(rows) == 1
        assert rows[0]["name"] == TEST_COMPANY_NAME


def test_select_company_two_filters():
    with db.connect() as connection:
        sql = text(
            "SELECT * FROM company WHERE is_active = :active AND id >= :id"
        )
        result = connection.execute(sql, {"active": True, "id": 65})
        rows = result.mappings().all()

        assert len(rows) >= 2
