from database.connection import get_meta_connection

def register_user(username: str, password: str) -> bool:
    """
    Insert a new user (plaintext password) into users table.
    Returns False if username already exists.
    """
    conn = get_meta_connection()
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM users WHERE username = %s", (username,))
    if cur.fetchone():
        cur.close()
        return False
    cur.execute(
        "INSERT INTO users(username, password) VALUES (%s, %s)",
        (username, password)
    )
    conn.commit()
    cur.close()
    return True

def verify_credentials(username: str, password: str) -> bool:
    """
    Verify plaintext password against users table.
    """
    conn = get_meta_connection()
    cur = conn.cursor()
    cur.execute("SELECT password FROM users WHERE username = %s", (username,))
    row = cur.fetchone()
    cur.close()
    return bool(row and row[0] == password)
