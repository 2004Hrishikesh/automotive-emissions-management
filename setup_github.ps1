# Setup GitHub Repository Script
# Run this script to initialize git and prepare for GitHub push

Write-Host "=== GitHub Repository Setup ===" -ForegroundColor Cyan
Write-Host ""

# Check if git is installed
try {
    $gitVersion = git --version 2>&1
    Write-Host "Git is installed" -ForegroundColor Green
} catch {
    Write-Host "Git is not installed. Please install Git first." -ForegroundColor Red
    exit 1
}

# Initialize git repository if not already initialized
if (-Not (Test-Path ".git")) {
    Write-Host "Initializing Git repository..." -ForegroundColor Yellow
    git init
    Write-Host "✓ Git repository initialized" -ForegroundColor Green
} else {
    Write-Host "✓ Git repository already initialized" -ForegroundColor Green
}

# Configure git (update with your details)
Write-Host ""
Write-Host "Configuring Git..." -ForegroundColor Yellow
$userName = Read-Host "Enter your GitHub username"
$userEmail = Read-Host "Enter your GitHub email"

git config user.name "$userName"
git config user.email "$userEmail"
Write-Host "✓ Git configured" -ForegroundColor Green

# Add all files
Write-Host ""
Write-Host "Adding files to git..." -ForegroundColor Yellow
git add .
Write-Host "✓ Files added" -ForegroundColor Green

# Create initial commit
Write-Host ""
Write-Host "Creating initial commit..." -ForegroundColor Yellow
git commit -m "Initial commit: Automotive Emissions Optimization - Phase I and II Complete"
Write-Host "Initial commit created" -ForegroundColor Green

# Instructions for GitHub
Write-Host ""
Write-Host "=== Next Steps ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Go to GitHub (https://github.com) and create a new repository named 'automotive-emissions-optimization'" -ForegroundColor White
Write-Host "2. Do NOT initialize with README, .gitignore, or license (we already have these)" -ForegroundColor White
Write-Host "3. Copy the repository URL (should be: https://github.com/$userName/automotive-emissions-optimization.git)" -ForegroundColor White
Write-Host ""
Write-Host "4. Then run these commands:" -ForegroundColor Yellow
Write-Host "   git remote add origin https://github.com/$userName/automotive-emissions-optimization.git" -ForegroundColor Cyan
Write-Host "   git branch -M main" -ForegroundColor Cyan
Write-Host "   git push -u origin main" -ForegroundColor Cyan
Write-Host ""
Write-Host "Or if you want to push to the existing repository (automotive-emissions-management):" -ForegroundColor Yellow
Write-Host "   git remote add origin https://github.com/2004Hrishikesh/automotive-emissions-management.git" -ForegroundColor Cyan
Write-Host "   git branch -M main" -ForegroundColor Cyan
Write-Host "   git push -u origin main" -ForegroundColor Cyan
Write-Host ""
Write-Host "Setup complete!" -ForegroundColor Green
