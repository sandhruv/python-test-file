import secrets
import sqlite3


def connect(db_path: str = "accounts.db") -> sqlite3.Connection:
    """Opens a connection with row access by column name."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(conn: sqlite3.Connection) -> None:
    """Creates the users and sessions tables if they do not exist yet."""
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            email TEXT NOT NULL UNIQUE
        );

        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            token TEXT NOT NULL UNIQUE,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        """
    )
    conn.commit()


def create_user(conn: sqlite3.Connection, email: str) -> int:
    """Creates a user and returns its id."""
    cursor = conn.execute("INSERT INTO users (email) VALUES (?)", (email,))
    conn.commit()
    return int(cursor.lastrowid)


def create_session(conn: sqlite3.Connection, user_id: int) -> str:
    """Issues a new session token for a user."""
    token = secrets.token_urlsafe(32)
    conn.execute(
        "INSERT INTO sessions (user_id, token) VALUES (?, ?)",
        (user_id, token),
    )
    conn.commit()
    return token


def get_session(conn: sqlite3.Connection, token: str):
    """Looks up an active session by token."""
    return conn.execute(
        "SELECT * FROM sessions WHERE token = ?", (token,)
    ).fetchone()


def delete_user(conn: sqlite3.Connection, user_id: int) -> None:
    """Deletes a user account."""
    conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()


def count_sessions(conn: sqlite3.Connection, user_id: int) -> int:
    """Returns how many sessions belong to a user."""
    row = conn.execute(
        "SELECT COUNT(*) AS n FROM sessions WHERE user_id = ?", (user_id,)
    ).fetchone()
    return int(row["n"])
