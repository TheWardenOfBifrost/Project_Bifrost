# MVP Specification – Project Bifrost

## 🎯 Formål
MVP (Minimum Viable Product) skal bevise Bifrosts kerneøkonomi gennem et simpelt flow:
- F2P spil → Locked runes
- Locked runes → Unlocked runes
- Unlocked runes → Withdraw (admin-godkendt)

MVP skal være simpelt, testbart og køre udelukkende på **Wallet1 (Main Payout Wallet)**, som manuelt fyldes op med STARS i starten.

---

## 🏗️ Systemkomponenter

### Wallets
- **Wallet1 (Main Payout Wallet)**  
  - Indeholder alle midler (test-funds).  
  - Bruges til withdraws.  
  - Ingen staking i MVP.  

### Runes
- **Locked Runes (F2P)**  
  - Spilles ind på gratis bane (ingen indskud).  
  - Har ingen værdi i sig selv, men bruges som buy-in i næste kamp.  
  - Tabes hvis spilleren taber.  
  - Kan konverteres til Unlocked, hvis spilleren vinder.  

- **Unlocked Runes**  
  - Vindes ved at konvertere Locked (ved sejr).  
  - Kan anmodes til withdraw.  
  - Har reel værdi, da de kan sendes til on-chain adresse (via admin approval).  

---

## ⚙️ Flows

### 1. F2P → Locked
- Spiller deltager i en gratis bane.  
- Reward: Locked runes til spillerens konto.  

### 2. Locked → Unlocked
- Spiller bruger Locked runes som buy-in i kamp.  
- Efter kamp:  
  - Vinder → Locked konverteres til Unlocked.  
  - Taber → Locked går tabt.  

### 3. Withdraw (Unlocked → on-chain)
- Spiller anmoder om withdraw fra Unlocked.  
- Admin godkender eller afviser.  
- Ved godkendelse udbetales fra Wallet1 til spillerens adresse.  
- Alle events logges i audit-log.  

---

## 🔒 Regler (MVP Core)
- Kun **Wallet1** bruges i MVP.  
- **Alle withdraws kræver admin approval.**  
- **Ingen auto-withdraw** direkte til kæden.  
- **Alle bevægelser logges** (F2P → Locked, Locked → Unlocked, Withdraws).  
- **Kun STARS** understøttet i MVP.  

---

## ✅ Deliverables
- [ ] Simpel datamodel for Locked/Unlocked balances pr. spiller.  
- [ ] F2P flow → Locked runes.  
- [ ] Locked → Unlocked flow (med kampresultat).  
- [ ] Withdraw flow (Unlocked → Wallet1 → on-chain, med admin approval).  
- [ ] Audit-log system (CSV eksport).  
- [ ] Admin UI (simpelt: balances, pending withdraws, logs).  
- [ ] Unit tests for core flows.  

---

## 📊 Fremtidige Noter (ikke i MVP)
- Wallet2 (staking pools og yield).  
- Forskellige coins (ATOM, ENJ, m.fl.).  
- NFT marketplace.  
- Anti-cheat system.  
- Faceit-integration.  
