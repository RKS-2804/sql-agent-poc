# test_db.py
from database.connection import get_data_connection

conn = get_data_connection()
print("OK:", conn)
conn.close()
