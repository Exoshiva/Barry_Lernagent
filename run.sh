#!/bin/bash
# Startet den Ollama-Server im Hintergrund und dann die Python-App
# Ausführbar machen mit: chmod +x run.sh

echo "Starte Ollama-Server für Modell 'mistral' im Hintergrund..."
ollama run mistral &

echo "Starte EduShiva-Agenten aus dem Hauptverzeichnis..."
python3 -m app.main