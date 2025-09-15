from sqlalchemy import select, Engine
from sqlalchemy.orm import Session
from app.library.storage.models import History
from datetime import datetime

class DietHistory:
    def __init__(self, engine: Engine):
        self.engine = engine
    def GetHistory(self, user_id: int, start: datetime, end: datetime)-> list[History]:
        with Session(self.engine) as session:
            stmt = select(History).\
                where(History.line_id == user_id).\
                where(History.created_at >= start).\
                where(History.created_at < end)
            result = session.scalars(stmt).all()
            return result
    def AddHistory(self, history: History) -> History:
        with Session(self.engine) as session:
            session.add(history)
            session.commit()
            session.refresh(history)
            return history

