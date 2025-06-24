import sqlite3
import os

DATABASE_NAME = 'edushiva.db'

def init_db():
    """
    Initialisiert die Datenbank und erstellt die Tabellen gemäß schema.sql.
    Die Datenbank wird im Hauptverzeichnis des Projekts erstellt.
    """
    # Stelle sicher, dass wir uns im Hauptverzeichnis des Projekts befinden
    # damit die DB-Datei am richtigen Ort landet.
    db_path = os.path.join(os.path.dirname(__file__), '..', DATABASE_NAME)
    schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')

    try:
        # Verbindung zur Datenbank herstellen (erstellt die Datei, wenn sie nicht existiert)
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print(f"Datenbank verbunden unter: {db_path}")

        # Lese das Schema aus der .sql-Datei
        with open(schema_path, 'r', encoding='utf-8') as f:
            sql_script = f.read()
        
        # Führe das SQL-Skript aus (kann mehrere Befehle enthalten)
        cursor.executescript(sql_script)
        conn.commit()
        
        print("Datenbankschema erfolgreich initialisiert.")
        
        # Test: Lese die eben eingefügten Daten
        cursor.execute("SELECT * FROM learning_progress;")
        rows = cursor.fetchall()
        print("Aktueller Lernfortschritt:")
        for row in rows:
            print(row)

        conn.close()
        
    except sqlite3.Error as e:
        print(f"Ein Fehler bei der Datenbankinitialisierung ist aufgetreten: {e}")
    except FileNotFoundError:
        print(f"Fehler: Die Schema-Datei unter {schema_path} wurde nicht gefunden.")


if __name__ == '__main__':
    # Erlaubt uns, dieses Skript auch direkt zum Testen auszuführen
    init_db()

