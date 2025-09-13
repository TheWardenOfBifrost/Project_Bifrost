# tools/seed_db.py
import argparse
import os
import sqlite3
import subprocess
import sys

BACKEND_DIR = os.path.dirname(os.path.dirname(__file__))
DB_PATH = os.path.join(BACKEND_DIR, "bifrost.db")

def run(cmd: list[str]) -> int:
    print(">", " ".join(cmd))
    return subprocess.call(cmd, cwd=BACKEND_DIR)

def ensure_db():
    if not os.path.exists(DB_PATH):
        print("DB not found. Running: alembic upgrade head")
        code = run([sys.executable, "-m", "alembic", "upgrade", "head"])
        if code != 0:
            print("ERROR: Could not initialize DB via alembic.", file=sys.stderr)
            sys.exit(code)

def reset_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print("Deleted bifrost.db")
    code = run([sys.executable, "-m", "alembic", "upgrade", "head"])
    if code != 0:
        print("ERROR: alembic failed.", file=sys.stderr)
        sys.exit(code)
    print("DB reset + migrated ✅")

def with_conn():
    ensure_db()
    con = sqlite3.connect(DB_PATH)
    con.execute("PRAGMA foreign_keys=ON")
    return con

def add_asset(code: str, a_type: str = "fungible", asset_id: int | None = None):
    con = with_conn()
    cur = con.cursor()
    if asset_id is None:
        # create with AUTOINCREMENT by omitting id
        cur.execute(
            "INSERT OR IGNORE INTO assets(code, type, metadata_json) VALUES (?, ?, NULL)",
            (code, a_type),
        )
    else:
        cur.execute(
            "INSERT OR IGNORE INTO assets(id, code, type, metadata_json) VALUES (?, ?, ?, NULL)",
            (asset_id, code, a_type),
        )
    con.commit(); con.close()
    print(f"✅ Asset ensured: {code} ({a_type})")

def set_balance(user_id: int, asset_code: str, amount: int):
    con = with_conn()
    cur = con.cursor()
    # ensure asset exists and fetch id
    cur.execute("SELECT id FROM assets WHERE code = ?", (asset_code,))
    row = cur.fetchone()
    if not row:
        cur.execute(
            "INSERT INTO assets(code, type, metadata_json) VALUES (?, 'fungible', NULL)",
            (asset_code,),
        )
        asset_id = cur.lastrowid
    else:
        asset_id = row[0]

    # upsert a balance: use REPLACE on a stable synthetic id or do a select first
    cur.execute(
        "SELECT id FROM user_balances WHERE user_id=? AND asset_id=?",
        (user_id, asset_id),
    )
    r = cur.fetchone()
    if r:
        cur.execute("UPDATE user_balances SET amount=? WHERE id=?", (amount, r[0]))
    else:
        cur.execute(
            "INSERT INTO user_balances(user_id, asset_id, amount) VALUES (?, ?, ?)",
            (user_id, asset_id, amount),
        )
    con.commit(); con.close()
    print(f"✅ Balance set: user {user_id} → {asset_code} = {amount}")

def seed_defaults():
    add_asset("DUST", "fungible", asset_id=1)
    set_balance(1, "DUST", 420)
    print("✅ Seeded defaults (user_id=1, DUST=420)")

def show(user_id: int | None):
    con = with_conn()
    cur = con.cursor()

    print("\nASSETS")
    for row in cur.execute("SELECT id, code, type FROM assets ORDER BY id"):
        print(" ", row)

    if user_id is not None:
        print(f"\nBALANCES for user {user_id}")
        for row in cur.execute("""
            SELECT a.code, ub.amount
            FROM user_balances ub
            JOIN assets a ON a.id = ub.asset_id
            WHERE ub.user_id=?
            ORDER BY a.code
        """, (user_id,)):
            print(" ", row)
    con.close()
    print()

def main():
    ap = argparse.ArgumentParser(description="Seed / manage local bifrost.db (SQLite)")
    ap.add_argument("--reset", action="store_true", help="Delete DB and run alembic upgrade head")
    ap.add_argument("--seed-defaults", action="store_true", help="Create DUST and give user 1 some balance")
    ap.add_argument("--add-asset", nargs=2, metavar=("CODE", "TYPE"), help="Add asset (e.g. DUST fungible)")
    ap.add_argument("--set-balance", nargs=3, metavar=("USER_ID", "ASSET_CODE", "AMOUNT"), help="Set a user's balance")
    ap.add_argument("--show", nargs="?", const="0", metavar="USER_ID", help="Show assets and balances (optional user_id)")

    args = ap.parse_args()

    if args.reset:
        reset_db()

    if args.seed_defaults:
        seed_defaults()

    if args.add_asset:
        code, a_type = args.add_asset
        add_asset(code, a_type)

    if args.set_balance:
        uid, code, amt = args.set_balance
        set_balance(int(uid), code, int(amt))

    if args.show is not None:
        uid = None if args.show == "0" else int(args.show)
        show(uid)

if __name__ == "__main__":
    main()
