# # 📂 Repo Structure – Project Bifrost

Denne fil giver et hurtigt overblik over, hvordan mapper og filer i repoet er organiseret.

---

## Root (øverste niveau)

- **docs/** → Al dokumentation
- **mvp/** → MVP-projektkode (backend + frontend senere)
- **endgame/** → Planer/filer til fremtidige funktioner
- **tools/** → Hjælpeværktøjer og scripts
- **.gitignore** → Git konfiguration (hvad der skal ignoreres)

---

## docs/

Her ligger alt skriftligt materiale.

- **specs/** → whitepapers, MVP- og endgame-specs, kædeoversigt
  - mvp_spec.md  
  - endgame_spec.md  
  - CHAINS.md
- **TECH_OVERVIEW.md** → overblik over programmer, sprog og flows
- **TEST_FLOW.md** → trin-for-trin guide til at teste API’et (cURL)
- **REPO_STRUCTURE.md** → denne fil (mappeplan)

---

## mvp/

Her bygger vi den første kørende version.

- **backend/** → FastAPI backend
  - src/api/main.py → selve API’et
  - equirements.txt → Python-pakker
  - .venv/ → virtuelt Python-miljø (lokalt, ikke på GitHub)
- **frontend/** → React-admin panel (kommer senere)

---

## endgame/

Alt hvad der skal bruges, når Wallet2, staking og multichain kommer ind i spillet.  
Her parkeres idéer, filer og prototyper, så de ikke roder i MVP.

---

## tools/

Scripts, hjælpefiler og evt. automation, der kan bruges til udvikling, tests eller drift.

---

# Huskeregel

- **docs/** = “alt på skrift”  
- **mvp/** = “alt der kører nu”  
- **endgame/** = “alt til fremtiden”  
- **tools/** = “alt der hjælper”  

