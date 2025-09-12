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

# 🧰 Project Bifrost – Toolbox

## VS Code Genveje

- **Ctrl + S** → Gem filer (standard)
- **F6** → Quick Push  
  → Kører `tools/quick_commit.ps1` → `git add/commit/push` med auto-besked
- **F5** → Start/Stop API-server (debug)  
  → Starter `uvicorn src.api.main:app` på port 8000/8001  
  → Stop med den røde knap eller Shift+F5
- **Ctrl + Alt + R** → Start API-server (uden debug, som task)  
  → Stop i terminalen med `Ctrl+C`

## Healthcheck

- Tjek serverstatus: [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health)  
  → Skal svare med `{ "ok": true }`

## Notes

- Interpreter skal være sat til:  
  `mvp/backend/.venv/Scripts/python.exe`
- Hvis F5 fejler med “ModuleNotFoundError” → vælg interpreter igen:  
  `Ctrl+Shift+P` → *Python: Select Interpreter*
- Hvis port 8000 er optaget → skift til 8001 i `.vscode/launch.json`.
