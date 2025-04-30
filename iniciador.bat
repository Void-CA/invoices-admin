@echo off
cd /d "%~dp0"
docker-compose up -d

:: Ejecutar el servidor de impresión sin mostrar la ventana del CMD
start "" pythonw "printing_server/app.py"
