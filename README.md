# Barry: Der KI-Lernagent

**Barry ist ein KI-Agent in Python, der lernt, SQL-Abfragen basierend auf natürlicher Sprache zu erstellen und auszuführen.**

![Barry in Aktion](pfad/zum/screenshot.gif)

## Features

Feature 1: Interagiert mit einer SQL-Datenbank, um dynamisch Daten basierend auf komplexen Anfragen abzurufen und aufzubereiten.

Feature 2: Nutzt lokal laufende Sprachmodelle via Ollama, um Anfragen in natürlicher Sprache in präzise, ausführbare SQL-Abfragen zu übersetzen.

Feature 3: Bietet ein schnelles Prototyping-Interface mit Gradio, um eine interaktive Konversation mit dem Agenten zu ermöglichen und die Datenbankergebnisse darzustellen.

## Getting Started

Folge diesen Schritten, um Barry auf deinem System zum Laufen zu bringen.

### Voraussetzungen

* Python 3.9+
* **Ollama muss lokal installiert und gestartet sein.** (Anleitung unter [ollama.com](https://ollama.com/))
* Ein heruntergeladenes Ollama-Modell, das für die Anwendung genutzt wird (z.B. `ollama pull mistral`).

### Installation & Start

1.  **Klone das Repository:**
    ```bash
    git clone [https://github.com/Exoshiva/Barry_Lernagent.git](https://github.com/Exoshiva/Barry_Lernagent.git)
    ```
2.  **Gehe in das Projektverzeichnis:**
    ```bash
    cd Barry_Lernagent
    ```
3.  **Installiere die Abhängigkeiten:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Starte den Agenten:**
    * Für Windows: `run.bat`
    * Für Linux/Mac: `bash run.sh`

## Benutzung

Nach dem Start, öffne deinen Browser und gehe zu `http://127.0.0.1:7860`. Dort kannst du Barry eine Frage in natürlicher Sprache stellen.
