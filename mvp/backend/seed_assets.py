# mvp/backend/seed_assets.py

from sqlmodel import Session, select, SQLModel
from src.api.deps import engine
from src.api.models import Asset, AssetKind


def ensure(session: Session, code: str, kind: AssetKind, decimals: int) -> None:
    """Insert asset if it does not already exist."""
    exists = session.exec(select(Asset).where(Asset.code == code)).first()
    if not exists:
        session.add(
            Asset(
                code=code,
                kind=kind,
                decimals=decimals,
                is_active=True,
            )
        )


def main() -> None:
    # 1) Sørg for at alle tabeller findes
    SQLModel.metadata.create_all(engine)

    # 2) Indsæt start-assets, hvis de mangler
    with Session(engine) as s:
        ensure(s, "STARS", AssetKind.coin, 6)
        ensure(s, "DUST", AssetKind.soft, 2)
        ensure(s, "SHARD", AssetKind.craft, 0)

        # RUNES som selvstændige assets (ingen scope)
        ensure(s, "LOCKED_RUNE", AssetKind.soft, 2)
        ensure(s, "UNLOCKED_RUNE", AssetKind.soft, 2)

        s.commit()

    print("Seeded STARS, DUST, SHARD, LOCKED_RUNE, UNLOCKED_RUNE.")


if __name__ == "__main__":
    main()

