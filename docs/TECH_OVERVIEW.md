# 🛠️ Tech Overview – Project Bifrost

## 📂 Generel struktur
- **Git + GitHub**  
  Styrer versioner af projektet (kode, dokumenter, flowcharts).  
  → Du arbejder lokalt i VS Code, og `git push` sender det til GitHub.

- **Visual Studio Code (VS Code)**  
  Dit værktøj til at skrive kode, README’er og styre filer.  

---

## 💻 Backend (MVP)
- **Sprog: Python 3**  
- **Framework: FastAPI** → laver API’er (fx `/health`).  
- **Webserver: Uvicorn** → kører FastAPI lokalt.  
- **Virtuelt miljø (.venv)** → sandbox til Python pakker.  

---

## 🎨 Frontend (senere)
- **Sprog: JavaScript (eller TypeScript)**  
- **Framework: React** → simpelt Admin Panel.  

---

## 📜 Docs
- **Markdown (.md)** → README, specs, cheat sheets.  
- **Flowcharts (PNG/SVG)** → visuelle diagrammer i `/docs/flowcharts/`.  

---

## 🔗 Blockchain / Wallets
- **Wallet1** = Main payout wallet (bruges i MVP).  
- **Wallet2** = Staking wallet (kommer i Endgame).  
- **Stars (STARS)** = Første coin vi leger med.  
- **Locked runes** = Fås via F2P, bruges som buy-in.  
- **Unlocked runes** = Vindes ved sejr, kan withdrawes.  

---

## 🚦 Workflow for dig (kort sagt)
1. Skriv/ret filer i VS Code.  
2. Start backend lokalt for at teste endpoints.  
3. Commit + push → ændringer vises på GitHub.  
4. Test i browseren (http://127.0.0.1:8000).  

---

## 🤔 Typiske kommandoer
- Tjek Python version: `python --version`  
- Start server:
