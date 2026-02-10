Param()
Set-StrictMode -Version Latest
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

Write-Host "Pulling latest from git (main)..."
git pull origin main 2>$null

Write-Host "Building and starting containers..."
docker-compose up -d --build --remove-orphans

Write-Host "Waiting for backend health (http://localhost:8000/health)..."
$ok = $false
for ($i=0; $i -lt 30; $i++) {
  try {
    Invoke-WebRequest -UseBasicParsing -Uri "http://localhost:8000/health" -TimeoutSec 2 | Out-Null
    Write-Host "Backend healthy."
    $ok = $true
    break
  } catch {}
  Start-Sleep -Seconds 2
}
if (-not $ok) {
  Write-Warning "Backend did not become healthy in time."
  docker-compose ps
  docker-compose logs --tail 200 backend
  exit 1
}
