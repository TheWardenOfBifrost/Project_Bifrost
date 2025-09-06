Write-Host "Resetting repo to last commit..." -ForegroundColor Yellow
git reset --hard
git clean -fd
Write-Host "Done." -ForegroundColor Green
