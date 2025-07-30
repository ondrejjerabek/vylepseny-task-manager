
import mysql.connector

def pripoj_databazi():
    try:
        spojeni = mysql.connector.connect(
            host="localhost",
            user="root",
            password="heslo",  # Uprav dle tvé konfigurace
            database="ukol_db"
        )
        return spojeni
    except mysql.connector.Error as err:
        print("Chyba při připojení k databázi:", err)
        return None

def pridat_ukol(spojeni):
    nazev = input("Zadejte název úkolu: ")
    popis = input("Zadejte popis úkolu: ")
    stav = input("Zadejte stav úkolu (např. nové, hotovo): ")
    termin = input("Zadejte termín (YYYY-MM-DD): ")

    kurzor = spojeni.cursor()
    sql = "INSERT INTO ukoly (nazev, popis, stav, termin) VALUES (%s, %s, %s, %s)"
    data = (nazev, popis, stav, termin)
    kurzor.execute(sql, data)
    spojeni.commit()
    print("Úkol byl přidán.")

def zobrazit_ukoly(spojeni):
    kurzor = spojeni.cursor()
    kurzor.execute("SELECT * FROM ukoly")
    vysledky = kurzor.fetchall()
    if not vysledky:
        print("Žádné úkoly nebyly nalezeny.")
    for ukol in vysledky:
        print(ukol)

def aktualizovat_ukol(spojeni):
    id_ukolu = input("Zadejte ID úkolu k aktualizaci: ")
    novy_stav = input("Zadejte nový stav úkolu: ")

    kurzor = spojeni.cursor()
    sql = "UPDATE ukoly SET stav = %s WHERE id = %s"
    data = (novy_stav, id_ukolu)
    kurzor.execute(sql, data)
    spojeni.commit()
    print("Úkol byl aktualizován.")

def odstranit_ukol(spojeni):
    id_ukolu = input("Zadejte ID úkolu k odstranění: ")
    kurzor = spojeni.cursor()
    sql = "DELETE FROM ukoly WHERE id = %s"
    data = (id_ukolu,)
    kurzor.execute(sql, data)
    spojeni.commit()
    print("Úkol byl odstraněn.")

def hlavni_menu():
    spojeni = pripoj_databazi()
    if not spojeni:
        return

    while True:
        print("\n--- Task Manager ---")
        print("1. Přidat úkol")
        print("2. Zobrazit úkoly")
        print("3. Aktualizovat úkol")
        print("4. Odstranit úkol")
        print("5. Konec")
        volba = input("Zadejte volbu: ")

        if volba == "1":
            pridat_ukol(spojeni)
        elif volba == "2":
            zobrazit_ukoly(spojeni)
        elif volba == "3":
            aktualizovat_ukol(spojeni)
        elif volba == "4":
            odstranit_ukol(spojeni)
        elif volba == "5":
            spojeni.close()
            print("Ukončuji program.")
            break
        else:
            print("Neplatná volba.")

if __name__ == "__main__":
    hlavni_menu()
