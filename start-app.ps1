# For Windows PowerShell
Write-Host "Starting VAT CRM application (backend and frontend)..." -ForegroundColor Green

# Start the backend in a new PowerShell window
Start-Process powershell -ArgumentList "-NoExit -Command `"cd '$PSScriptRoot'; `$env:FLASK_APP = 'backend.app:create_app'; `$env:FLASK_ENV = 'development'; flask run --host=0.0.0.0 --port=8000`""

Write-Host "Backend server starting at http://localhost:8000" -ForegroundColor Cyan
Start-Sleep -Seconds 2

# Determine which frontend to use (new_frontend if it exists, otherwise frontend)
$frontendPath = "$PSScriptRoot\new_frontend"
if (-not (Test-Path $frontendPath)) {
    $frontendPath = "$PSScriptRoot\frontend"
}

# Start the frontend in a new PowerShell window
Start-Process powershell -ArgumentList "-NoExit -Command `"cd '$frontendPath'; npm run dev`""

Write-Host "Frontend development server starting..." -ForegroundColor Cyan
Write-Host "`nApplication is now running:" -ForegroundColor Green
Write-Host "- Backend: http://localhost:8000" -ForegroundColor White
Write-Host "- Frontend: Check the terminal window for URL (typically http://localhost:5173)" -ForegroundColor White
Write-Host "`nPress Ctrl+C in the respective terminal windows to stop the servers." -ForegroundColor Yellow
