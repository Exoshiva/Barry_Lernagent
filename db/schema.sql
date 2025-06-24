-- SQL-Befehle zum Erstellen unserer Tabellen.
-- CREATE TABLE IF NOT EXISTS stellt sicher, dass wir keine Fehler bekommen, wenn die Tabelle schon existiert.

CREATE TABLE IF NOT EXISTS learning_progress (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    topic TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL CHECK(status IN ('not_started', 'in_progress', 'completed')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Optional: Ein paar Beispieldaten einfügen, um zu sehen, dass es funktioniert.
-- INSERT OR IGNORE stellt sicher, dass wir keine doppelten Einträge erstellen.
INSERT OR IGNORE INTO learning_progress (topic, status) VALUES ('SQL Grundlagen', 'not_started');
INSERT OR IGNORE INTO learning_progress (topic, status) VALUES ('Python Basics', 'not_started');
