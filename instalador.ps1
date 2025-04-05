# Verifica si Docker está instalado
if (!(Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Host "Docker no está instalado. Iniciando instalación..."

    $dockerInstallerUrl = "https://desktop.docker.com/win/main/amd64/Docker Desktop Installer.exe"
    $installerPath = "$env:TEMP\DockerInstaller.exe"

    Invoke-WebRequest -Uri $dockerInstallerUrl -OutFile $installerPath
    Write-Host "Instalador descargado. Ejecutando instalación..."
    Start-Process -FilePath $installerPath -ArgumentList "install", "--quiet" -Wait

    Write-Host "Instalación de Docker finalizada. Reinicia tu computadora e intenta de nuevo."
    exit
} else {
    Write-Host "Docker ya está instalado."
}

# Inicia Docker Desktop (si no está iniciado)
$dockerDesktopPath = "$env:ProgramFiles\Docker\Docker\Docker Desktop.exe"
if (!(Get-Process -Name "Docker Desktop" -ErrorAction SilentlyContinue)) {
    Write-Host "Iniciando Docker Desktop..."
    Start-Process -FilePath "$dockerDesktopPath"
    Start-Sleep -Seconds 10
}

# Esperar a que Docker esté verdaderamente listo
$maxRetries = 20
$retries = 0
while ($retries -lt $maxRetries) {
    try {
        $versionInfo = docker version --format '{{.Server.Version}}' 2>$null
        if ($versionInfo) {
            Write-Host "Docker está listo con versión $versionInfo"
            break
        }
    } catch {
        Write-Host "Esperando a que Docker se estabilice ($retries/$maxRetries)..."
    }
    Start-Sleep -Seconds 5
    $retries++
}

if ($retries -eq $maxRetries) {
    Write-Host "Docker no se estabilizó a tiempo. Verifica si hay errores manualmente."
    exit
}


if ($retries -eq 0) {
    Write-Host "Docker no se pudo iniciar. Por favor, revisa Docker Desktop manualmente."
    exit
}

# Ejecutar docker-compose
Write-Host "Iniciando los servicios con Docker Compose..."
docker-compose up -d
