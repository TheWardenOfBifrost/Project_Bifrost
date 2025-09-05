# Project Bifrost
# 🌉 Project Bifrost

## Vision
Project Bifrost bygger bro mellem **gaming** og **staking-økonomi**.  
Målet er at skabe et bæredygtigt system hvor spillere, supportere og partnere kan deltage i en transparent og fair økonomi, drevet af staking-yield og Locked/Unlocked runes.

- Første coin i systemet: **STARS** (store tal = mere dopamin).  
- Andre chains (ATOM, ENJ, m.fl.) kommer senere.  
- MVP skal være **simpelt, sikkert og testbart** før vi bygger mere på.

> "Fate chooses those who dare to cross."

---

## 📂 Repo Struktur
- `/docs` → Whitepapers, flowcharts, specs  
- `/mvp` → Minimum Viable Product (økonomi core)  
- `/endgame` → Fremtidige features (multichain, marketplace, anti-cheat osv.)  
- `/tools` → Scripts, calculators, migration utils  

---

## 🚀 MVP Core (skal bygges først)
1. **Wallet & Balancer**
   - Wallet1 (staking) + Wallet2 (operations) flow
   - Daglig/manuel compounding (ingen auto withdraw til kæden)

2. **Locked/Unlocked Runes**
   - Locked buy-in check før kamp
   - Resultat → Locked → Unlocked (intern flytning)

3. **Payout Engine**
   - Manuel udbetaling fra Unlocked til ekstern on-chain adresse
   - Admin-approval (ingen auto withdraw i MVP)

4. **Stars først**
   - STARS yield tracking, daglig rate, cron-job til compounding

5. **Audit Log**
   - Alle bevægelser logges (Locked ↔ Unlocked, withdraws, approvals)
   - Eksport til CSV for revision

6. **Admin Panel (simpelt)**
   - Se saldi
   - Godkende/afvise withdraws
   - Eksportér data

---

## 🎮 MVP+ (Onboarding/F2P flow – nice to have)
Ikke kritisk for første MVP, men vigtigt næste skridt:

- F2P spillere kan tjene en **lille mængde Unlocked** dagligt.  
- Disse kan bruges til at købe deres første Locked runes.  
- Flow:  
  **F2P → lidt Unlocked → Locked → deltag i rigtige kampe**.  

➡️ Dette viser fuld cirkel og gør onboarding mere smooth, men kan vente til efter MVP Core er stabil.

---

## 🛠️ Endgame – Fremtidige Features
Langsigtede mål, ikke i MVP:

- Multichain support (ATOM, ENJ, OSMO, m.fl.)  
- NFT Marketplace (Runes + maps på eftermarkedet, *ikke hosting-NFTs*)  
- Faceit-integration og matchmaking  
- Anti-cheat + risk scoring system  
- Partner staking pools + revenue share  
- Full launcher integration (Unity/Unreal, Discord bots, dashboards)  

---

## 📐 Standards
- **Branching**:  
  - `main` = stabil  
  - `dev` = integration  
  - `feat/*`, `fix/*` = feature branches  

- **Commits**: Conventional Commits (`feat:`, `fix:`, `chore:`, `docs:` …)  

- **Env**: `.env` filer med eksempel i `mvp/backend/.env.sample`  

---

## 🖥️ Opsætning (lokalt)
1. Klon repoet:  
   ```bash
   git clone https://github.com/TheWardenOfBifrost/Project_Bifrost.git
   cd Project_Bifrost
