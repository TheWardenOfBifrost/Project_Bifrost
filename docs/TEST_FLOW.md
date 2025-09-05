# TEST_FLOW (MVP)

## 0) Check server
Open http://127.0.0.1:8000/docs

## 1) F2P → LOCKED
curl -X POST "http://127.0.0.1:8000/f2p" -H "Content-Type: application/json" -d "{\"player_id\":\"player123\",\"reward_locked\":10}"

Expect: locked=10, unlocked=0

## 2) Balance
curl -X GET "http://127.0.0.1:8000/balance/player123"

## 3) Match: LOCKED → UNLOCKED (win)
curl -X POST "http://127.0.0.1:8000/locked-to-unlocked" -H "Content-Type: application/json" -d "{\"player_id\":\"player123\",\"locked_spent\":10,\"result\":\"win\"}"

Expect: locked=0, unlocked=10

## 4) Withdraw (creates pending)
curl -X POST "http://127.0.0.1:8000/withdraw" -H "Content-Type: application/json" -d "{\"player_id\":\"player123\",\"amount\":5,\"address\":\"stars1xxxxxxxxxxxxxxxxxxxx\"}"

Expect: status=pending, unlocked=5

## 5) Admin – view pending
curl -X GET "http://127.0.0.1:8000/admin/pending?admin_token=secret123"

## 6) Admin – approve
curl -X POST "http://127.0.0.1:8000/admin/approve" -H "Content-Type: application/json" -d "{\"request_id\":1,\"approve\":true,\"admin_token\":\"secret123\"}"

Expect: status=approved, tx_hash=SIMULATED_TX_1

## Notes
- Use a new player_id to test fresh balances (memory resets on server restart).
- Admin token (demo): secret123
