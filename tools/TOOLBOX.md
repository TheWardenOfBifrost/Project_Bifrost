# 🛠️ Tools – Project Bifrost

Her samler vi scripts, små værktøjer og idéer, der hjælper udvikling og drift.

## 1. Git & Repo
- **quick_commit.ps1** → genvej til `git add .` + `git commit` + `git push`
- **reset_repo.ps1** → nulstiller working dir til seneste commit (`git reset --hard` + `git clean -fd`)

## 2. Backend (Python / FastAPI)
Start server:


cd mvp\backend
..venv\Scripts\activate
python -m uvicorn src.api.main:app --reload --port 8000


## 3. Testing (eksempler)
- tools/tests/f2p.ps1 → F2P (giver LOCKED)
- tools/tests/match_win.ps1 → Locked → Unlocked
- tools/tests/withdraw.ps1 → Pending withdraw
- tools/tests/admin_approve.ps1 → Godkender id=1

## 4. Drift (senere)
- Wallet refill checker
- Fee estimator
- Address validator
