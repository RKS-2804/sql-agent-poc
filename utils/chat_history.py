from database.connection import get_meta_connection

def fetch_history_from_db(username: str) -> list[dict]:
    """
    Load all prior messages (role & text) for this user.
    """
    conn = get_meta_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT role, message FROM chat_history "
        "WHERE username = %s ORDER BY id ASC",
        (username,)
    )
    rows = cur.fetchall()
    cur.close()
    return [{"role": r[0], "message": r[1]} for r in rows]

def save_message(username: str, role: str, message: str) -> None:
    """
    Append one chat message to history.
    """
    conn = get_meta_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO chat_history(username, role, message) VALUES (%s, %s, %s)",
        (username, role, message)
    )
    conn.commit()
    cur.close()
