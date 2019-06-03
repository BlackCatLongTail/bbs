import functools
import uuid
import time
from flask import (
    session,
    request,
    render_template,
    redirect,
    url_for,
)

from models.user import User
from utils import log


def current_user():
    # 从 session 中找到 user_id 字段, 找不到就 -1
    # 然后 User.find_by 来用 id 找用户
    # 找不到就返回 None
    uid = session.get('user_id', -1)
    u = User.one(id=uid)
    if u is not None:
        return u
    else:
        return User.guest()


def same_user_required(func):
    # 对用户信息进行修改，需要进行权限认证
    @functools.wraps(func)
    def inner(*args, **kwargs):
        if request.method == 'POST':
            user_id = int(request.form.get('user_id'))
        else:
            user_id = int(request.args.get('user_id'))

        u = current_user()
        print('user_id is {}'.format(user_id), type(user_id))
        print('u.id is {}'.format(u.id), type(u.id))
        if u.id == user_id:
            return func(*args, **kwargs)
        else:
            return render_template('no_permission.html', u=u)

    return inner


def login_required(func):
    # 需要登录
    @functools.wraps(func)
    def inner(*args, **kwargs):
        u_id = session.get('user_id', None)

        if u_id is None:
                return redirect(url_for("user.login_view"))
        else:
            e = User.exist(id=u_id)
            if e:
                return func(*args, **kwargs)
            else:
                return redirect(url_for("user.login_view"))

    return inner


def make_csrf_token(u):
    csrf_token = str(uuid.uuid4())
    session[csrf_token] = u.id
    return csrf_token


def csrf_token_required(func):
    # 需要验证csrf_token的有效性
    @functools.wraps(func)
    def inner(*args, **kwargs):
        if request.method == 'POST':
            csrf_token = request.form.get("csrf_token", None)
            log('csrf_token_required_token', csrf_token)

        else:
            csrf_token = request.args.get("csrf_token", None)
            log('csrf_token_required_token', csrf_token)

        u = current_user()

        if csrf_token in session and session[csrf_token] == u.id:
            # 移除csrf_token，确保验证码的唯一性
            session.pop(csrf_token)
            log('csrf_token_required 验证，通过')
            return func(*args, **kwargs)
        else:
            log('csrf_token_required 验证，未通过')
            return render_template('no_permission.html', u=u)

    return inner


def year_month_day(second):
    # 将秒转化为年月日分时
    year = second//(3600 * 24 * 30 * 12)
    month = second//(3600 * 24 * 30)
    day = second//(3600 * 24)
    hour = second//3600
    minute = second//60

    if year > 1 or year == 1:
        return '{}年前'.format(year)
    else:
        if month > 1 or month == 1:
            return '{}月前'.format(month)
        else:
            if day > 1 or day == 1:
                return '{}日前'.format(day)
            else:
                if hour > 1 or hour == 1:
                    return '{}时前'.format(hour)
                else:
                    if minute > 1 or minute == 1:
                        return '{}分前'.format(minute)
                    else:
                        return '{}秒前'.format(second)


def trans_time(t):
    # 将时间戳转化为年月日的形式,方便阅读
    m = time.localtime(t)
    return '{}年{}月{}日{}时'.format(m.tm_year, m.tm_mon, m.tm_mday, m.tm_hour)


