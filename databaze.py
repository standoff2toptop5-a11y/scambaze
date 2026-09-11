# ==============================
# SOURCE LIGHT — DATABASE
# ==============================

import sqlite3


DB_NAME = "sourcelight.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            telegram_id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            role TEXT NOT NULL DEFAULT 'user'
        )
    """)

    conn.commit()
    conn.close()


def add_or_update_user(
    telegram_id: int,
    username: str | None,
    first_name: str | None
):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT telegram_id FROM users WHERE telegram_id = ?",
        (telegram_id,)
    )

    exists = cursor.fetchone()

    if exists:
        cursor.execute("""
            UPDATE users
            SET username = ?, first_name = ?
            WHERE telegram_id = ?
        """, (
            username,
            first_name,
            telegram_id
        ))
    else:
        cursor.execute("""
            INSERT INTO users
            (telegram_id, username, first_name, role)
            VALUES (?, ?, ?, 'user')
        """, (
            telegram_id,
            username,
            first_name
        ))

    conn.commit()
    conn.close()


def get_user_by_id(telegram_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT telegram_id, username, first_name, role
        FROM users
        WHERE telegram_id = ?
    """, (telegram_id,))

    user = cursor.fetchone()

    conn.close()

    return user


def get_user_by_username(username: str):
    username = username.lstrip("@").lower()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT telegram_id, username, first_name, role
        FROM users
        WHERE LOWER(username) = ?
    """, (username,))

    user = cursor.fetchone()

    conn.close()

    return user


def set_role(telegram_id: int, role: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE users
        SET role = ?
        WHERE telegram_id = ?
    """, (
        role,
        telegram_id
    ))

    conn.commit()
    conn.close()
