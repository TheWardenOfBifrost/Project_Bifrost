param([string]$m = "")

$ErrorActionPreference = "Stop"

# Gå til repo-root
$repoRoot = (git rev-parse --show-toplevel).Trim()
Set-Location $repoRoot

# Auto-commit besked hvis tom
if ([string]::IsNullOrWhiteSpace($m)) {
    $branch = (git rev-parse --abbrev-ref HEAD).Trim()
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $m = "chore: quick save - $timestamp [$branch]"
}

git add -A

# Ingen tomme commits
$changes = (git status --porcelain)
if ([string]::IsNullOrWhiteSpace($changes)) {
    Write-Host "No changes. Skipping commit/push."
    exit 0
}

git commit -m $m

# Push (auto -u ved første push)
try {
    # Tjek for upstream-tracking; citér '@{u}' så PS ikke tror det er en hash
    git rev-parse --abbrev-ref --symbolic-full-name '@{u}' *> $null
    if ($LASTEXITCODE -eq 0) {
        git push
    } else {
        git push -u origin $branch
    }
} catch {
    git push -u origin $branch
}
