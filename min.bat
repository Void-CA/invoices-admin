@echo off
cd /d "%~dp0"

echo Iniciando Docker Compose... >> log.txt
docker compose up --build -d >> log.txt 2>&1

pause
