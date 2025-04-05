@echo off
REM Cambia el directorio al de tu proyecto
cd %~dp0

REM Ejecuta docker compose down para detener y eliminar los contenedores
docker-compose down

REM Pausa para que puedas ver cualquier mensaje
pause
