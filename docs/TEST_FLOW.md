# TEST_FLOW (MVP)

## 0) Check server
http://127.0.0.1:8000/docs

## 1) F2P → LOCKED
curl -X POST "http://127.0.0.1:8000/f2p" -H "Content-Type: application/json" -d "{\"player_id\":\"player123\",\"reward_locked\":10}"

## 2) Balance
curl -X GET "http://127.0.0.1:8000/balance/player123"

## 3) Match: LOCKED → UNLOCKED (win)
curl -X POST "http://127.0.0.1:8000/locked-to-unlocked" -H "Content-Type: application/json" -d "{\"player_id\":\"player123\",\"locked_spent\":10,\"result\":\"win\"}"

## 4) Withdraw (pending)
curl -X POST "http://127.0.0.1:8000/withdraw" -H "Content-Type: application/json" -d "{\"player_id\":\"player123\",\"amount\":5,\"address\":\"stars1xxxxxxxxxxxxxxxxxxxx\"}"

## 5) Admin – view pending
curl -X GET "http://127.0.0.1:8000/admin/pending?admin_token=secret123"

## 6) Admin – approve
curl -X POST "http://127.0.0.1:8000/admin/approve" -H "Content-Type: application/json" -d "{\"request_id\":1,\"approve\":true,\"admin_token\":\"secret123\"}"
