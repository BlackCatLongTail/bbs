from models.user import User
from sqlalchemy import Column, String
from models import SQLMixin, SQLBase
import sqlalchemy


class Reply(SQLMixin, SQLBase):
    __tablename__ = 'Reply'
    content = Column(String(200), nullable=False)
    topic_id = Column(sqlalchemy.Integer, nullable=False)
    user_id = Column(sqlalchemy.Integer, nullable=False)

    def user(self):
        u = User.one(id=self.user_id)
        return u

    @staticmethod
    def recently_reply(rs):
        # reply按照updated_time时间排序后，返回第一条回复
        rs = sorted(rs, key=lambda r: r.updated_time, reverse=True)
        if len(rs) < 1:
            return None
        else:
            return rs[0]

