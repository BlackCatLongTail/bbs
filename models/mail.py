from sqlalchemy import Column, String
from models import SQLMixin, SQLBase
import sqlalchemy
from routes import User
from utils import log


class Mail(SQLMixin, SQLBase):
    __tablename__ = 'Mail'
    title = Column(String(200), nullable=False)
    content = Column(String(400), nullable=False)
    sender_id = Column(sqlalchemy.Integer, nullable=False)
    receiver_id = Column(sqlalchemy.Integer, nullable=False)

    @classmethod
    def new(cls, form):
        receiver_name = form.get('receiver_name')
        log('in mail receiver_name', receiver_name)
        receiver = User.one(username=receiver_name)

        if receiver is not None:
            form['receiver_id'] = receiver.id
            m = super().new(**form)
            return m, '邮件发送成功'
        else:
            return None, '邮件发送失败，请检查收件人名字是否正确'
