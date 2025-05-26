import pandas as pd
from database.connection import get_data_connection as get_connection

def run_sql_query(sql: str) -> pd.DataFrame | None:
    """
    Execute the SQL against synthetic_sales_data.
    Returns a DataFrame for SELECT queries, else None.
    """
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(sql)
        rows = cur.fetchall()
        cols = [desc[0] for desc in cur.description]
        df = pd.DataFrame(rows, columns=cols)
    except Exception:
        df = None
    finally:
        conn.commit()
        cur.close()
    return df
