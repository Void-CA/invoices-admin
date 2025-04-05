@echo off
REM Cambia el directorio al de tu proyecto usando una ruta relativa
cd %~dp0

REM Ejecuta docker compose up
docker-compose up --build

REM Pausa para que puedas ver cualquier error o mensaje
pause
