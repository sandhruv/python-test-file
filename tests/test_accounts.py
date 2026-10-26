import sqlite3

import pytest

from src.accounts import (
    connect,
    count_sessions,
    create_session,
    create_user,
    delete_user,
    get_session,
    init_db,
)


@pytest.fixture
def conn():
    connection = connect(":memory:")
    init_db(connection)
    yield connection
    connection.close()


def test_create_user_and_session(conn):
    user_id = create_user(conn, "alice@example.com")
    token = create_session(conn, user_id)
    session = get_session(conn, token)
    assert session["user_id"] == user_id
    assert count_sessions(conn, user_id) == 1


def test_delete_user(conn):
    user_id = create_user(conn, "bob@example.com")
    create_session(conn, user_id)
    delete_user(conn, user_id)
    remaining = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    assert remaining == 0


def test_duplicate_email_rejected(conn):
    create_user(conn, "carol@example.com")
    with pytest.raises(sqlite3.IntegrityError):
        create_user(conn, "carol@example.com")
