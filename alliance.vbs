Set WshShell = CreateObject("WScript.Shell")
' Ejecutar el archivo .bat
WshShell.Run ".\iniciar_app.bat", 0, False

' Mostrar un mensaje indicando que la app está disponible
WshShell.Popup "La aplicación esta lista para usar.", 5, "Notificación", 64
