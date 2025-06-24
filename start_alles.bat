@echo off
REM Setzt den Titel des Konsolenfensters
title Barry Launcher

echo --- Starte die Ollama KI-Modelle ---
echo.
echo Ein neues Fenster fuer das MISTRAL-Modell wird geoeffnet...
start "Ollama Mistral" cmd /c "echo Starte MISTRAL... && ollama run mistral"

echo Ein neues Fenster fuer das LLAVA-Modell wird geoeffnet...
start "Ollama Llava" cmd /c "echo Starte LLAVA... && ollama run llava"
echo.

echo --- Warte, bis die KI-Modelle geladen sind ---
echo Dies kann einen Moment dauern, besonders beim ersten Mal.
echo Warte 30 Sekunden...

REM Dieser Befehl pausiert das Skript für 30 Sekunden.
REM Passen Sie diesen Wert bei Bedarf an (z.B. auf 60), wenn Ihr Computer mehr Zeit benötigt.
timeout /t 30 /nobreak >nul
echo.

echo --- Starte die Barry-Anwendung ---
python -m app.main

echo.
echo Barry wurde gestartet. Falls die App abstuerzt, ueberpruefen Sie dieses Fenster auf Fehlermeldungen.
pause
