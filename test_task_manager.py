
import mysql.connector
import pytest

def test_pripojeni_k_db():
    try:
        spojeni = mysql.connector.connect(
            host="localhost",
            user="root",
            password="heslo",
            database="ukol_db"
        )
        assert spojeni.is_connected()
    except:
        pytest.fail("Nepodařilo se připojit k databázi")

def test_vlozeni_ukolu():
    spojeni = mysql.connector.connect(
        host="localhost",
        user="root",
        password="heslo",
        database="ukol_db"
    )
    kurzor = spojeni.cursor()
    sql = "INSERT INTO ukoly (nazev, popis, stav, termin) VALUES (%s, %s, %s, %s)"
    data = ("Test", "Test popis", "nové", "2025-12-31")
    kurzor.execute(sql, data)
    spojeni.commit()
    assert kurzor.rowcount == 1
    spojeni.close()
