import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import URL, create_engine, text
from sqlalchemy.orm import Session

from database import get_db
from main import app


TEST_DB_NAME = "hotel_operations_test"

test_url = URL.create(
    drivername="postgresql+psycopg",
    username=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST", "127.0.0.1"),
    port=int(os.getenv("DB_PORT", "5432")),
    database=TEST_DB_NAME,
)

test_engine = create_engine(test_url)


@pytest.fixture
def client():
    connection = test_engine.connect()

    try:
        # Verify the database we actually connected to.
        connected_database = connection.execute(
            text("SELECT current_database()")
        ).scalar_one()

        if connected_database != TEST_DB_NAME:
            raise RuntimeError(
                f"Unsafe test database: {connected_database}"
            )

        connection.rollback()
        transaction = connection.begin()

        session = Session(
            bind=connection,
            join_transaction_mode="create_savepoint",
        )

        def override_get_db():
            yield session

        app.dependency_overrides[get_db] = override_get_db

        try:
            with TestClient(app) as test_client:
                yield test_client
        finally:
            app.dependency_overrides.pop(get_db, None)
            session.close()
            transaction.rollback()

    finally:
        connection.close()