# Endgame Specification – Project Bifrost

## 🎯 Formål
Endgame-versionen af Bifrost bygger ovenpå MVP’en og tilføjer de systemer, der gør projektet til en fuld skalerbar økonomi.  
Her er fokus på multichain, staking-yield, marketplace og eksterne integrationer (fx Faceit).

---

## 🏗️ Systemkomponenter

### Wallets
- **Wallet1 (Main Payout Wallet)**  
  - Samme rolle som i MVP → udbetalingsbuffer.  
  - Godkendte withdraws sendes herfra.  

- **Wallet2 (Staking Wallet)**  
  - Styrer staking pools på forskellige chains.  
  - Modtager yield → sender regelmæssigt til Wallet1, så der er likviditet til payouts.  
  - Styrer compound og multi-wallet flows.  

### Runes & Currencies
- **Locked Runes (Buy-in)**  
  - Bruges til at deltage i kampe.  
  - Taber mister Locked, vinder konverterer til Unlocked.  

- **Unlocked Runes (Rewards)**  
  - Vindes gennem Locked kampe.  
  - Kan bruges in-game eller withdrawes til kæden.  

- **Shards, Dust, andre interne valutaer**  
  - Bruges til crafting, progression og shop-systemer.  
  - Konverteringer styres gennem definerede flows.  

---

## ⚙️ Nøgleflows

### 1. Multichain Staking
- Støtte for flere coins (fx STARS, ATOM, ENJ).  
- Hver spiller knytter en adresse pr. kæde.  
- Yield fra Wallet2 → sendes til Wallet1 for udbetalinger.  

### 2. Marketplace
- Spillere kan handle NFTs (fx runes, maps, skins).  
- Eftermarked tilladt for maps, men **hosting-NFTs forbliver låst**.  
- Integration med fx Enjin Marketplace.  

### 3. Anti-cheat & Risk Scoring
- Kampresultater krydstjekkes mod anti-cheat.  
- Brugere kan tildeles en risiko-score (fx ved mistænkelig aktivitet).  

### 4. Faceit Integration
- Mulighed for at integrere med eksterne turneringsplatforme.  
- Bruger Bifrosts Locked/Unlocked model til at håndtere buy-in og payouts.  

### 5. Admin & Ops
- Admin kan overvåge alle wallets, staking pools og marketplace.  
- Drift-flow: supporter contribution, refill cycle, auto-scaling.  

---

## 🔒 Regler (Endgame)
- Wallet1 bruges kun til udbetaling (ikke staking).  
- Wallet2 står for staking + compounding.  
- Alle withdraws kræver fortsat admin approval (evt. automatisering på sigt).  
- Alle events logges (Wallet2 → Wallet1, Locked ↔ Unlocked, Withdraws, Marketplace).  

---

## ✅ Deliverables
- [ ] Wallet2 staking + multi-chain support.  
- [ ] Compound og auto-scaling scripts.  
- [ ] Marketplace (NFT trading, med locked hosting-NFTs).  
- [ ] Anti-cheat system + risk scoring integration.  
- [ ] Faceit integration (matchmaking + payouts).  
- [ ] Full admin dashboard (wallets, pools, marketplace).  
- [ ] End-to-end tests af flows.  

---

## 📊 Fremtidige Noter
- Mulighed for partner staking pools.  
- Revenue share model (fx 10–20% til Wallet1).  
- Integration med eksterne launchers (Unity/Unreal, Discord bots).  
