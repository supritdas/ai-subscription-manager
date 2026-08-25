import sqlite3
from pathlib import Path



BASE_DIR = Path(__file__).resolve().parent.parent


DB_PATH = BASE_DIR / "subscriptions.db"


def get_connection():
    """Create and return a connection to the SQLite database."""
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    """Create the required database tables if they do not exist."""

    connection = get_connection()


    connection.execute("""
        CREATE TABLE IF NOT EXISTS subscriptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            cost REAL NOT NULL,
            renewal_date TEXT,
            active INTEGER NOT NULL DEFAULT 1
        )
    """)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def add_subscription(name, cost, renewal_date=None):
    """Add a new subscription to the database."""

    connection = get_connection()

    connection.execute(
        """
        INSERT INTO subscriptions (name, cost, renewal_date)
        VALUES (?, ?, ?)
        """,
        (name, cost, renewal_date)
    )

    connection.commit()
    connection.close()


def get_all_subscriptions():
    """Return all active subscriptions."""

    connection = get_connection()

    rows = connection.execute(
        """
        SELECT id, name, cost, renewal_date, active
        FROM subscriptions
        WHERE active = 1
        ORDER BY id
        """
    ).fetchall()

    connection.close()

    return [dict(row) for row in rows]


def get_monthly_total():
    """Calculate the total monthly cost of active subscriptions."""

    connection = get_connection()

    row = connection.execute(
        """
        SELECT COALESCE(SUM(cost), 0) AS total
        FROM subscriptions
        WHERE active = 1
        """
    ).fetchone()

    connection.close()

    return row["total"]


def set_budget(budget):
    """Save or update the user's monthly subscription budget."""

    connection = get_connection()

    connection.execute(
        """
        INSERT INTO settings (key, value)
        VALUES ('monthly_budget', ?)
        ON CONFLICT(key)
        DO UPDATE SET value = excluded.value
        """,
        (str(budget),)
    )

    connection.commit()
    connection.close()


def get_budget():
    """Return the user's monthly subscription budget."""

    connection = get_connection()

    row = connection.execute(
        """
        SELECT value
        FROM settings
        WHERE key = 'monthly_budget'
        """
    ).fetchone()

    connection.close()

    if row is None:
        return None

    return float(row["value"])