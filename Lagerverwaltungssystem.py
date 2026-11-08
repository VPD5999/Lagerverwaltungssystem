import sqlite3
from pathlib import Path 

print("Willkommen im Lagerverwaltungssystem!")
print()

datenbank_pfad = Path(__file__).resolve().parent / "lager.db"

verbindung = sqlite3.connect(datenbank_pfad) 
cursor=verbindung.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS artikel( 
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    menge INTEGER NOT NULL
)
""")

verbindung.commit()


while True: 
    print()
    print("Was möchten Sie tun? ")
    print()
    print("(1): Ware Hinzufügen? ")
    print("(2): Ware Entnehmen? ")
    print("(3): Lagerbestand Anzeigen? ")
    print("(4): Artikel löschen? ")
    print("(5): Programm Beenden? ")

    eingabe=input("Bitte wähle aus: ").strip()

    if not eingabe.isdigit():
        print("Ungültige Eingabe. Bitte geben Sie eine Zahl von 1 bis 5 ein.")
        continue
    eingabe = int(eingabe)

    if eingabe == 1:
        while True:
            ware = input("Welche Ware möchten Sie hinzufügen? ").strip() 
            if ware:
                break
            print("Der Artikelname darf nicht leer sein.")

        while True:
            menge_eingabe = input("Menge? ").strip()
            if menge_eingabe.isdigit():
                menge = int(menge_eingabe)
                if menge > 0:
                    break
            print("Ungültige Eingabe. Bitte geben Sie eine gültige Zahl ein.")

        cursor.execute(
            "SELECT id, menge FROM artikel WHERE name = ? COLLATE NOCASE",
            (ware,)
        )

        artikel=cursor.fetchone()

        if artikel:
            cursor.execute(
                "UPDATE artikel SET menge = menge + ? WHERE id = ?",
                (menge, artikel[0])
            )

            print(f"{menge} Stück {ware} wurden zum Lagerbestand hinzugefügt.")
        else:
            cursor.execute(
                "INSERT INTO artikel (name, menge) VALUES (?, ?)",
                (ware, menge)
            )
            print(f"{menge} Stück {ware} wurden im Lagerbestand neu angelegt.")

        verbindung.commit()
    
    elif eingabe == 2:
        while True:
            ware = input("Welche Ware möchten Sie entnehmen? ").strip()

            if ware:
                break

            print("Der Artikelname darf nicht leer sein.")

        cursor.execute(
            "SELECT id, menge FROM artikel WHERE name = ? COLLATE NOCASE", (ware,)
        )
        artikel = cursor.fetchone()
        if artikel:
            aktuelle_menge = artikel[1]
            while True:
                menge_eingabe = input("Menge? ").strip()
                if menge_eingabe.isdigit():
                    menge = int(menge_eingabe)

                    if menge <= 0:
                     print("Ungültige Eingabe. Bitte geben Sie eine gültige Zahl ein.")
                     continue
                    if menge > aktuelle_menge:
                        print(f"Es sind nur {aktuelle_menge} Stück {ware} im Lagerbestand vorhanden. Bitte geben Sie eine gültige Menge ein.")
                        continue
                    break
                print("Ungültige Eingabe. Bitte geben Sie eine gültige Zahl ein.")

            cursor.execute(
                    "UPDATE artikel SET menge = menge - ? WHERE id = ?",
                    (menge, artikel[0])
            )
            verbindung.commit()
            print(f"{menge} Stück {ware} wurden aus dem Lagerbestand entnommen.")
        else:
            print(f"{ware} ist nicht im Lagerbestand vorhanden.")

    elif eingabe == 3:
        print("Der aktuelle Lagerbestand ist: ")

        cursor.execute("SELECT id, name, menge FROM artikel")
        artikel_liste = cursor.fetchall()

        for artikel in artikel_liste:
            print(f"- ID: {artikel[0]} | {artikel[1]} | Menge: {artikel[2]}")

    elif eingabe == 4:
        while True:
            ware = input("Welchen Artikel möchten Sie löschen? ").strip()
            if ware:
                break
            print("Der Artikelname darf nicht leer sein.")
        cursor.execute(
            "SELECT id, name FROM artikel WHERE name = ? COLLATE NOCASE", 
            (ware,)
        )
        artikel = cursor.fetchone()
        if artikel:
            print(f"Artikel gefunden {artikel[1]}")
            while True:
                bestaetigung = input("Wollen Sie den Artikel wirklich löschen? (ja/nein) ").strip().lower()

                if bestaetigung in ("ja","nein"):
                    break
                print("Ungültige Eingabe. Bitte geben Sie 'ja' oder 'nein' ein.")

            if bestaetigung=="ja":
                    cursor.execute(
                    "DELETE FROM artikel WHERE id = ?", 
                    (artikel[0],)
                    )
                    verbindung.commit()
                    print(f"Artikel {artikel[1]} wurde gelöscht.")
            elif bestaetigung=="nein":
                    print("Löschen abgebrochen.")

        else:
            print(f"{ware} ist nicht im Lagerbestand vorhanden.")



    elif eingabe == 5:
        print("Das Programm wird beendet.")
        verbindung.close()
        break
    else:
        print("Ungültige Eingabe. Bitte wählen Sie eine gültige Option.")