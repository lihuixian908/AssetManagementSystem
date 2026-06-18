from app.models.asset import Asset
from app.repositories.base import BaseRepository


class AssetRepository(BaseRepository[Asset]):
    def __init__(self):
        super().__init__(Asset)

    def get_by_asset_code(self, db, asset_code: str) -> Asset | None:
        from sqlalchemy import select
        query = select(Asset).where(Asset.asset_code == asset_code)
        result = db.execute(query)
        return result.scalar_one_or_none()