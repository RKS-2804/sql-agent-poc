import os
from dotenv import load_dotenv
from database.connection import DATA_URI
from langchain_community.utilities import SQLDatabase
from langchain_community.tools.sql_database.tool import (
    ListSQLDatabaseTool,
    InfoSQLDatabaseTool,
)

load_dotenv()

db = SQLDatabase.from_uri(DATA_URI)

list_tables_tool = ListSQLDatabaseTool(db=db)
info_tables_tool = InfoSQLDatabaseTool(db=db)

def list_tables() -> str:
    """
    Return comma-separated table names from synthetic_sales_data.
    """
    return list_tables_tool.run("")

def get_schema_overview() -> str:
    """
    Return schema definitions for all tables.
    """
    tables = list_tables()
    return info_tables_tool.run(tables)
