from sqlmodel import Session, select, SQLModel
from src.api.deps import engine
from src.api.models import Asset, AssetKind

# 1) Sørg for at alle tabeller findes
SQLModel.metadata.create_all(engine)

# 2) Indsæt start-assets, hvis de mangler
with Session(engine) as s:
    def ensure(code, kind, decimals):
        exists = s.exec(select(Asset).where(Asset.code == code)).first()
        if not exists:
            s.add(Asset(code=code, kind=kind, decimals=decimals, is_active=True))

    ensure("STARS", AssetKind.coin, 6)
    ensure("DUST", AssetKind.soft, 2)
    ensure("SHARD", AssetKind.craft, 0)
    s.commit()

print("Seeded STARS/DUST/SHARD.")

