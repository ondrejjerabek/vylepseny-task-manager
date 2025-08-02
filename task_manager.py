
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

def validuj_neprazdny_vstup(prompt):
    while True:
        vstup = input(prompt).strip()
        if vstup:
            return vstup
        else:
            print("Tento údaj je povinný.")

def pridat_ukol():
    nazev = validuj_neprazdny_vstup("Zadejte název úkolu: ")
    popis = validuj_neprazdny_vstup("Zadejte popis úkolu: ")
    stav = validuj_neprazdny_vstup("Zadejte stav úkolu (např. nové, hotovo): ")
    termin = validuj_neprazdny_vstup("Zadejte termín (YYYY-MM-DD): ")

    with get_connection() as spojeni:
        kurzor = spojeni.cursor()
        try:
            kurzor.execute(
                "INSERT INTO ukoly (nazev, popis, stav, termin) VALUES (%s, %s, %s, %s)",
                (nazev, popis, stav, termin)
            )
            spojeni.commit()
            print("Úkol byl přidán.")
        except mysql.connector.Error as err:
            print("Chyba při přidávání úkolu:", err)

def zobrazit_ukoly():
    with get_connection() as spojeni:
        kurzor = spojeni.cursor()
        kurzor.execute("SELECT * FROM ukoly")
        vysledky = kurzor.fetchall()
        if not vysledky:
            print("Žádné úkoly nebyly nalezeny.")
        for ukol in vysledky:
            print(ukol)

def aktualizovat_ukol():
    zobrazit_ukoly()
    id_ukolu = validuj_neprazdny_vstup("Zadejte ID úkolu k aktualizaci: ")
    novy_stav = validuj_neprazdny_vstup("Zadejte nový stav úkolu: ")

    with get_connection() as spojeni:
        kurzor = spojeni.cursor()
        kurzor.execute(
            "UPDATE ukoly SET stav = %s WHERE id = %s", (novy_stav, id_ukolu)
        )
        spojeni.commit()
        print("Úkol byl aktualizován.")

def odstranit_ukol():
    zobrazit_ukoly()
    id_ukolu = validuj_neprazdny_vstup("Zadejte ID úkolu k odstranění: ")

    with get_connection() as spojeni:
        kurzor = spojeni.cursor()
        kurzor.execute("DELETE FROM ukoly WHERE id = %s", (id_ukolu,))
        spojeni.commit()
        print("Úkol byl odstraněn.")

def hlavni_menu():
    while True:
        print("\n--- Task Manager ---")
        print("1. Přidat úkol")
        print("2. Zobrazit úkoly")
        print("3. Aktualizovat úkol")
        print("4. Odstranit úkol")
        print("5. Konec")
        volba = input("Zadejte volbu: ")

        if volba == "1":
            pridat_ukol()
        elif volba == "2":
            zobrazit_ukoly()
        elif volba == "3":
            aktualizovat_ukol()
        elif volba == "4":
            odstranit_ukol()
        elif volba == "5":
            print("Ukončuji program.")
            break
        else:
            print("Neplatná volba.")

if __name__ == "__main__":
    hlavni_menu()
