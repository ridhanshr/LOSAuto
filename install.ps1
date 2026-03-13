# StatementGuard Installation Script
# This script installs the LOS Auto Suite / StatementGuard application.

$appName = "StatementGuard"
$repoUrl = "https://github.com/ridhanshr/StatementGuard"
$installDir = "$HOME\$appName"

Write-Host "Installing $appName..." -ForegroundColor Cyan

# 1. Create install directory
if (!(Test-Path $installDir)) {
    New-Item -ItemType Directory -Path $installDir | Out-Null
}

Set-Location $installDir

# 2. Check for Git
if (!(Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "Git not found. Installing Git via winget..." -ForegroundColor Yellow
    winget install --id Git.Git -e --source winget
}

# 3. Clone repository
Write-Host "Cloning repository..." -ForegroundColor Cyan
if (Test-Path ".git") {
    git pull origin main
} else {
    git clone $repoUrl .
}

# 4. Check for Node.js
if (!(Get-Command npm -ErrorAction SilentlyContinue)) {
    Write-Host "Node.js not found. Installing Node.js via winget..." -ForegroundColor Yellow
    winget install --id OpenJS.NodeJS -e --source winget
}

# 5. Install dependencies and Build
Write-Host "Setting up GUI..." -ForegroundColor Cyan
Set-Location "gui_modern"
npm install
npm run build

Write-Host "`nInstallation complete!" -ForegroundColor Green
Write-Host "To run the app, go to $installDir\gui_modern and run 'npm run electron'" -ForegroundColor White
