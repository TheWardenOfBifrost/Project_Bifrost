param([string]$m = "")

$ErrorActionPreference = "Stop"
$repoRoot = (git rev-parse --show-toplevel).Trim()
Set-Location $repoRoot

if ([string]::IsNullOrWhiteSpace($m)) {
    $branch = (git rev-parse --abbrev-ref HEAD).Trim()
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $m = "chore: quick save - $timestamp [$branch]"
}

git add -A
$changes = (git status --porcelain)
if ([string]::IsNullOrWhiteSpace($changes)) { Write-Host "No changes. Skipping commit/push."; exit 0 }

git commit -m $m

try {
    git rev-parse --abbrev-ref --symbolic-full-name '@{u}' *> $null
    if ($LASTEXITCODE -eq 0) { git push } else { git push -u origin $branch }
} catch {
    git push -u origin $branch
}
