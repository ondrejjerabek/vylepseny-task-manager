
import pytest
import mysql.connector
from contextlib import contextmanager

@contextmanager
def get_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="heslo",
        database="ukol_db"
    )
    try:
        yield connection
    finally:
        connection.close()

@pytest.fixture(autouse=True)
def cistici_fixtures():
    yield
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM ukoly")
        conn.commit()

def test_pridani_ukolu():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO ukoly (nazev, popis, stav, termin) VALUES ('Test', 'Popis', 'nove', '2025-12-31')")
        conn.commit()
        cursor.execute("SELECT * FROM ukoly WHERE nazev = 'Test'")
        assert cursor.fetchone() is not None

def test_odstraneni_ukolu():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO ukoly (nazev, popis, stav, termin) VALUES ('Delete', 'Popis', 'nove', '2025-12-31')")
        conn.commit()
        cursor.execute("DELETE FROM ukoly WHERE nazev = 'Delete'")
        conn.commit()
        cursor.execute("SELECT * FROM ukoly WHERE nazev = 'Delete'")
        assert cursor.fetchone() is None

def test_neplatny_termin():
    with pytest.raises(mysql.connector.Error):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO ukoly (nazev, popis, stav, termin) VALUES ('Chyba', 'Popis', 'nove', 'neplatne_datum')")
            conn.commit()
