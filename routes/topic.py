import time
from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
)

from routes import (
    current_user,
    csrf_token_required,
    login_required,
    make_csrf_token
)

from models.topic import Topic
from models.board import Board
from utils import log

main = Blueprint('topic', __name__)


@main.route('/<int:id>')
def detail(id):
    # http://localhost:3000/topic/1
    m = Topic.get(id)
    u = current_user()

    if not u.is_guest():
        csrf_token = make_csrf_token(u)
    else:
        csrf_token = ''

    log('detail_csrf_token is', csrf_token)
    created_time = time.localtime(m.created_time)
    return render_template("topic/detail.html", topic=m, u=u, ct=created_time, csrf_token=csrf_token)


@main.route("/add", methods=["POST"])
@login_required
@csrf_token_required
def add():
    form = request.form.to_dict()
    u = current_user()
    form['user_id'] = u.id
    m = Topic.new(**form)
    return redirect(url_for('.detail', id=m.id))


@main.route("/new")
@login_required
def new():
    # 发帖时, 实现对版块的选择, board_id是为了显示当前版块
    form = request.args
    print("board_id is [{}]".format(form.get('board_id', -1)))
    board_id = int(form.get('board_id', -1))
    bs = Board.all()

    u = current_user()
    csrf_token = make_csrf_token(u)
    log('topic.new csrf_token is', csrf_token)
    return render_template("topic/new.html", bid=board_id, bs=bs, csrf_token=csrf_token, u=u)


@main.route("/delete")
@login_required
@csrf_token_required
def delete():
    # 权限认证，只有本人或管理员才能删帖
    t_id = int(request.args.get('id'))
    t = Topic.one(id=t_id)
    u = current_user()

    if t.user_id == u.id or u.is_admin():
        result = Topic.delete(t_id)
        log('result is', result)
        return redirect('/')
    else:
        return render_template('no_permission.html', u=u)
