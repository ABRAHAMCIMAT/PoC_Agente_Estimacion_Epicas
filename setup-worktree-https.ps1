# Script para configurar el worktree con HTTPS
# Ejecutar como: .\setup-worktree-https.ps1

$worktreePath = "C:\Users\L03027810\repos\PoC_Agente_Estimacion_Epicas.worktrees\integrar-frontend-backend-excel-upload"

Write-Host "======================================" -ForegroundColor Cyan
Write-Host "Configurando Worktree con HTTPS" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

# 1. Navega al directorio del worktree
Write-Host "[1/6] Navegando al directorio del worktree..." -ForegroundColor Yellow
if (-not (Test-Path $worktreePath)) {
    Write-Host "⚠ El directorio no existe. Creándolo..." -ForegroundColor Yellow
    New-Item -ItemType Directory -Path $worktreePath -Force | Out-Null
}
cd $worktreePath

# 2. Inicializa el repositorio Git
Write-Host "[2/6] Inicializando repositorio Git..." -ForegroundColor Yellow
git init
if ($LASTEXITCODE -eq 0) { Write-Host "✓ Repositorio inicializado" -ForegroundColor Green } else { Write-Host "✗ Error en inicialización" -ForegroundColor Red }

# 3. Configura el remote origin
Write-Host "[3/6] Configurando remote origin con HTTPS..." -ForegroundColor Yellow
git remote add origin https://github.com/abrahamtec/PoC_Agente_Estimacion_Epicas.git
if ($LASTEXITCODE -eq 0) { Write-Host "✓ Remote configurado" -ForegroundColor Green } else { Write-Host "✗ Error al configurar remote" -ForegroundColor Red }

# 4. Descarga los cambios del repositorio remoto
Write-Host "[4/6] Descargando cambios del repositorio remoto..." -ForegroundColor Yellow
git fetch origin
if ($LASTEXITCODE -eq 0) { Write-Host "✓ Cambios descargados" -ForegroundColor Green } else { Write-Host "✗ Error en fetch" -ForegroundColor Red }

# 5. Cambia a la rama main y configúrala para seguir el remoto
Write-Host "[5/6] Cambiando a rama main..." -ForegroundColor Yellow
git checkout --track origin/main
if ($LASTEXITCODE -eq 0) { Write-Host "✓ Rama main configurada" -ForegroundColor Green } else { Write-Host "✗ Error al cambiar de rama" -ForegroundColor Red }

# 6. Verifica la configuración
Write-Host "[6/6] Verificando configuración..." -ForegroundColor Yellow
git branch -vv
Write-Host ""

Write-Host "======================================" -ForegroundColor Green
Write-Host "✓ Worktree configurado exitosamente" -ForegroundColor Green
Write-Host "======================================" -ForegroundColor Green
Write-Host ""
Write-Host "Información del repositorio:" -ForegroundColor Cyan
git remote -v
Write-Host ""
Write-Host "Rama actual:" -ForegroundColor Cyan
git branch --show-current
