from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "a7a2c2486db9"
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # assets: DUST, SHARD, BADGE osv.
    op.create_table(
        "assets",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("code", sa.String(64), unique=True, nullable=False),  # DUST, SHARD
        sa.Column("type", sa.String(32), nullable=False),               # fungible|nft|role
        sa.Column("metadata_json", sa.Text, nullable=True),
        sa.Column("created_at", sa.DateTime, server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
    )

    # user_balances: saldo pr. bruger pr. aktiv
    op.create_table(
        "user_balances",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("user_id", sa.Integer, nullable=False, index=True),
        sa.Column("asset_id", sa.Integer, nullable=False, index=True),
        sa.Column("amount", sa.BigInteger, nullable=False, server_default="0"),
        sa.Column("updated_at", sa.DateTime, server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.UniqueConstraint("user_id", "asset_id", name="uq_user_asset"),
        sa.ForeignKeyConstraint(["asset_id"], ["assets.id"], ondelete="CASCADE"),
    )

    # ledger: bogføring (sandheden). delta kan være negativ
    op.create_table(
        "ledger",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("tx_id", sa.String(64), nullable=False, unique=True, index=True),
        sa.Column("user_id", sa.Integer, nullable=False, index=True),
        sa.Column("asset_id", sa.Integer, nullable=False, index=True),
        sa.Column("delta", sa.BigInteger, nullable=False),
        sa.Column("reason", sa.String(64), nullable=True),      # e.g. shop_order, claim
        sa.Column("ref_id", sa.String(128), nullable=True),     # e.g. order_id / claim_id
        sa.Column("created_at", sa.DateTime, server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["asset_id"], ["assets.id"], ondelete="RESTRICT"),
    )

    # wallet_challenges: til sign-message flow
    op.create_table(
        "wallet_challenges",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("user_id", sa.Integer, nullable=False, index=True),
        sa.Column("challenge", sa.String(256), nullable=False),
        sa.Column("expires_at", sa.DateTime, nullable=True),
        sa.Column("used_at", sa.DateTime, nullable=True),
        sa.Column("created_at", sa.DateTime, server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
    )

    # wallet_links: linkede wallets
    op.create_table(
        "wallet_links",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("user_id", sa.Integer, nullable=False, index=True),
        sa.Column("chain", sa.String(16), nullable=False),   # evm|cosmos|enjin
        sa.Column("address", sa.String(128), nullable=False),
        sa.Column("verified_at", sa.DateTime, nullable=True),
        sa.Column("created_at", sa.DateTime, server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.UniqueConstraint("chain", "address", name="uq_chain_address"),
    )

    # payout_requests: udbetalinger (stub)
    op.create_table(
        "payout_requests",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("user_id", sa.Integer, nullable=False, index=True),
        sa.Column("asset_id", sa.Integer, nullable=False),
        sa.Column("amount", sa.BigInteger, nullable=False),
        sa.Column("dest_chain", sa.String(16), nullable=True),
        sa.Column("dest_address", sa.String(128), nullable=True),
        sa.Column("status", sa.String(16), nullable=False, server_default="submitted"),  # submitted|sent|confirmed|failed
        sa.Column("created_at", sa.DateTime, server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime, server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["asset_id"], ["assets.id"], ondelete="RESTRICT"),
    )

    # dex_routes: stub til DEX
    op.create_table(
        "dex_routes",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("from_asset", sa.String(64), nullable=False),
        sa.Column("to_asset", sa.String(64), nullable=False),
        sa.Column("route_json", sa.Text, nullable=True),
        sa.Column("enabled", sa.Boolean, nullable=False, server_default=sa.text("1")),
        sa.UniqueConstraint("from_asset", "to_asset", name="uq_dex_pair"),
    )

def downgrade():
    op.drop_table("dex_routes")
    op.drop_table("payout_requests")
    op.drop_table("wallet_links")
    op.drop_table("wallet_challenges")
    op.drop_table("ledger")
    op.drop_table("user_balances")
    op.drop_table("assets")
