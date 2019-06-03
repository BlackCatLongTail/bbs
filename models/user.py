import hashlib
import os
import uuid

from sqlalchemy import Column, String, Enum
from models import SQLMixin, SQLBase
from models.user_role import UserRole


class User(SQLMixin, SQLBase):
    __tablename__ = 'User'
    """
    User 是一个保存用户数据的 model
    现在只有两个属性 username 和 password
    """
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    signature = Column(String(200), default='Nothing.')
    avatar = Column(String(100), nullable=False, default='/user/avatar/1.jpg')
    role = Column(Enum(UserRole), nullable=False, default=UserRole.normal)

    def add_default_value(self):
        super().add_default_value()
        self.password = self.salted_password(self.password)

    @staticmethod
    def salted_password(password, salt='$!@><?>HUI&DWQa`'):
        salted = hashlib.sha256((password + salt).encode('ascii')).hexdigest()
        return salted

    @classmethod
    def register(cls, form):
        name = form.get('username', '')
        pwd = form.get('password', '')

        exist = User.exist(username=name)
        if exist:
            # 用户名必须唯一，发邮件需要用户名找user对象
            return None, '该用户名已存在'
        else:
            if len(name) > 2 and len(pwd) > 2:
                u = User.new(**form)
                return u, '注册成功'
            else:
                return None, '用户名长度需要大于2，密码长度需要大于2'

    @classmethod
    def validate_login(cls, form):
        query = dict(
            username=form['username'],
            password=User.salted_password(form['password']),
        )
        e = User.exist(**query)
        if e:
            return User.one(**query), '成功'
        else:
            return None, '用户名或密码错误'

    @classmethod
    def update_signature(cls, uid, form):
        u = super().update(uid, **form)
        return u, '成功'

    @classmethod
    def update_password(cls, uid, form):
        old_password = form["old_password"]
        new_password = form["new_password"]
        u = cls.one(id=uid)
        if u.password == cls.salted_password(old_password):
            if len(new_password) > 2:
                password = cls.salted_password(new_password)
                u = super().update(uid, password=password)
                return u, '成功'
            else:
                return None, '新密码长度需要大于2'
        else:
            return None, '旧密码不正确'

    @classmethod
    def update_avatar(cls, uid, file):
        suffix = file.filename.split('.')[-1]
        filename = '{}.{}'.format(str(uuid.uuid4()), suffix)
        path = os.path.join('avatars', filename)
        file.save(path)

        avatar_url = '/user/avatar/{}'.format(filename)  # wendy
        u = cls.update(uid, avatar=avatar_url)
        return u, '成功'

    @classmethod
    def guest(cls):
        u = cls()
        u.username = '游客'
        u.role = UserRole.guest
        return u

    def is_guest(self):
        return self.role is UserRole.guest

    def is_admin(self):
        return self.role is UserRole.admin


