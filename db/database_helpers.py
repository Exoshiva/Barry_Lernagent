import sqlite3
import os

DATABASE_NAME = 'edushiva.db'

def get_db_connection():
    """Stellt eine Verbindung zur Datenbank her und gibt das Connection-Objekt zurück."""
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(base_dir, '..', DATABASE_NAME)
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        print(f"Fehler beim Verbinden mit der Datenbank: {e}")
        return None

def get_all_progress():
    """Liest den gesamten Lernfortschritt aus der Datenbank aus."""
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT topic, status, created_at FROM learning_progress")
            progress_items = [dict(row) for row in cursor.fetchall()]
            conn.close()
            return progress_items
        except sqlite3.Error as e:
            print(f"Fehler beim Auslesen des Lernfortschritts: {e}")
            conn.close()
            return []
    return []

def update_progress_status(topic: str, new_status: str):
    """Aktualisiert den Status eines bestimmten Themas in der Datenbank."""
    valid_statuses = ['not_started', 'in_progress', 'completed']
    if new_status not in valid_statuses:
        print(f"Fehler: Ungültiger Status '{new_status}'.")
        return False
        
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE learning_progress SET status = ? WHERE topic = ?", (new_status, topic))
            conn.commit()
            print(f"Status für Thema '{topic}' erfolgreich auf '{new_status}' aktualisiert.")
            conn.close()
            return True
        except sqlite3.Error as e:
            print(f"Fehler beim Aktualisieren des Themas '{topic}': {e}")
            conn.close()
            return False
    return False

# --- NEUE FUNKTION HINZUGEFÜGT ---
def add_new_topic(topic_name: str):
    """Fügt ein neues Lernthema zur Datenbank hinzu."""
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            # INSERT OR IGNORE verhindert einen Fehler, falls das Thema bereits existiert
            cursor.execute("INSERT OR IGNORE INTO learning_progress (topic, status) VALUES (?, ?)", (topic_name, 'not_started'))
            conn.commit()
            print(f"Thema '{topic_name}' erfolgreich zur Datenbank hinzugefügt.")
            conn.close()
            return True
        except sqlite3.Error as e:
            print(f"Fehler beim Hinzufügen des Themas '{topic_name}': {e}")
            conn.close()
            return False
    return False

if __name__ == '__main__':
    print("--- Teste Datenbank-Helferfunktionen ---")
    print("\n1. Füge neues Thema 'Datenbanken' hinzu:")
    add_new_topic('Datenbanken')

    print("\n2. Lese allen aktuellen Fortschritt:")
    all_items = get_all_progress()
    if all_items:
        for item in all_items:
            print(f"  - Thema: {item['topic']}, Status: {item['status']}")
