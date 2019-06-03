from flask import (
    render_template,
    request,
    Blueprint,
)
from routes import (
    current_user,
)

from models.topic import Topic
from models.board import Board
from utils import log

main = Blueprint('index', __name__)


"""
用户在这里可以
    访问首页
    注册
    登录

用户登录后, 会写入 session, 并且定向到 /profile
"""


@main.route("/")
def index():
    form = request.args
    board_id = form.get('board_id', -1)
    board_id = int(board_id)

    if board_id == -1:
        # 访问主页，显示所有的ts
        ts = Topic.all()
    else:
        # 返回版块下的ts，无论board_id是否有效都能处理
        ts = Topic.all(board_id=board_id)

    u = current_user()
    bs = Board.all()
    # 传入board_id是为了让点击的版块呈现选中的效果
    return render_template("index.html", ts=ts, u=u, bs=bs, board_id=board_id)

