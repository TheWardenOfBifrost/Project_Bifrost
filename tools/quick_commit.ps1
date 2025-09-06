param([string]$m = "update")
git add .
git commit -m "$m"
git push
