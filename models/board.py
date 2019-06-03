from models.topic import Topic
from models import SQLMixin, SQLBase
from sqlalchemy import Column, String


class Board(SQLMixin, SQLBase):
    __tablename__ = 'Board'

    title = Column(String(50), nullable=False)

    def topics(self):
        ts = Topic.all(board_id=self.id)
        return ts

