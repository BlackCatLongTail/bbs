from models.user import User
from models.reply import Reply
from models import SQLMixin, SQLBase
from sqlalchemy import Column, String
import sqlalchemy


class Topic(SQLMixin, SQLBase):
    __tablename__ = 'Topic'

    views = Column(sqlalchemy.Integer, nullable=False, default=0)
    title = Column(String(50), nullable=False)
    content = Column(String(725), nullable=False)
    user_id = Column(sqlalchemy.Integer, nullable=False)
    board_id = Column(sqlalchemy.Integer, nullable=False)

    @classmethod
    def get(cls, id):
        m = cls.one(id=id)
        m.views += 1
        m.save()
        return m

    def user(self):
        u = User.one(id=self.user_id)
        return u

    def replies(self):
        ms = Reply.all(topic_id=self.id)
        return ms

    def reply_count(self):
        count = len(self.replies())
        return count

    @staticmethod
    def no_repeat(ts):
        l = []
        s = set()
        for t in ts:
            if t.id not in s:       # 注意，我们以 id 来判断是否重复
                l.append(t.id)
                s.add(t.id)

        return [Topic.one(id=t_id) for t_id in l]

    @classmethod
    def recently_created_topic(cls, u):
        ts = cls.all(user_id=u.id)
        sorted_ts = sorted(ts, key=lambda t: t.created_time, reverse=True)
        return sorted_ts

    @classmethod
    def recently_replied_topic(cls, u):
        # 先拿到创建的所有回复，再根据回复拿到对应的topic，user->reply->topic
        rs = Reply.all(user_id=u.id)
        sorted_rs = sorted(rs, key=lambda r: r.created_time, reverse=True)

        ts = [cls.one(id=r.topic_id) for r in sorted_rs]
        print('ts')
        [print(t.id) for t in ts]
        sorted_ts = cls.no_repeat(ts)
        print('after')
        [print(t.id) for t in sorted_ts]
        return sorted_ts

    @classmethod
    def delete(cls, id):
        # 删除帖子下所有评论
        rs = Reply.all(topic_id=id)
        for r in rs:
            Reply.delete(r.id)
        # 删除帖子
        super().delete(id)
        return '成功删除'

