import sqlite3
import pytest

@pytest.fixture
def db_mem_connection():
    connection = sqlite3.connect(":memory:")
    cursor = connection.cursor()
    
    cursor.execute("""
        CREATE TABLE testing (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        )
    """)
    connection.commit()
    
    yield connection
    
    connection.close()