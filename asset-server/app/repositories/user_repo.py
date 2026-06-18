from app.models.user import User
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self):
        super().__init__(User)

    def get_by_username(self, db, username: str) -> User | None:
        from sqlalchemy import select
        query = select(User).where(User.username == username)
        result = db.execute(query)
        return result.scalar_one_or_none()