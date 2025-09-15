from sqlalchemy import select, Engine
from sqlalchemy.orm import Session
from app.library.storage.models import User

class UserObject:
    def __init__(self, engine: Engine):
        self.engine = engine
    def GetUserInfo(self, line_id: str)-> list[User]:
        with Session(self.engine) as session:
            stmt = select(User).\
                where(User.line_id == line_id)
            result = session.scalars(stmt).all()
            return result
    def AddUser(self, user: User) -> User:
        with Session(self.engine) as session:
            session.add(user)
            session.commit()
            session.refresh(user)
            return user
