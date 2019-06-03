import time
from flask import (
    render_template,
    request,
    redirect,
    session,
    url_for,
    Blueprint,
    abort,
    send_from_directory
)
from routes import (
    same_user_required,
    current_user,
    login_required,
    csrf_token_required,
    make_csrf_token,
    trans_time
)

from models.reply import Reply
from models.user import User
from models.topic import Topic

from utils import log

main = Blueprint('user', __name__)


@main.route("/register/view")
def register_view():
    # result是提交表单与否的依据，为None说明没有提交；不为None说明提交
    result = session.pop('result', None)
    success = session.pop('success', None)
    log('result', result)
    log('success', success)

    return render_template('user/register.html', result=result, success=success)


@main.route("/register", methods=['POST'])
def register():
    form = request.form.to_dict()
    # 用类函数来判断
    u, result = User.register(form)
    success = u is not None

    session['result'] = result
    session['success'] = success
    return redirect(url_for('.register_view'))


@main.route("/login/view")
def login_view():
    # result是提交表单与否的依据，为None说明没有提交；不为None说明提交
    result = session.pop('result', None)
    success = session.pop('success', None)
    log('result', result)
    log('success', success)

    return render_template('user/login.html', result=result, success=success)


@main.route("/login", methods=['POST'])
def login():
    form = request.form
    u, result = User.validate_login(form)
    if u is not None:
        # session 中写入 user_id
        session['user_id'] = u.id
        # 设置 cookie 有效期为 永久
        session.permanent = True

    success = u is not None
    # result用来表明表单提交与否，success表示结果成功与否
    session['result'] = result
    session['success'] = success
    return redirect(url_for('.login_view'))


@main.route("/<int:id>")
def user_detail(id):
    # 由id找到博主，访问博主的主页, 显示最近话题
    author = User.one(id=id)
    current_u = current_user()
    if author is None:
        abort(404)
    else:
        created_topics = Topic.recently_created_topic(author)
        replied_topics = Topic.recently_replied_topic(author)

        return render_template("user/index.html",
                               created_topics=created_topics,
                               replied_topics=replied_topics,
                               author=author,
                               current_u=current_u,
                               User=User,
                               Reply=Reply,
                               trans_time=trans_time)


@main.route('/avatar/<filename>')
def avatar(filename):
    return send_from_directory('avatars', filename)


@main.route('/setting')
@login_required
def setting():
    # 返回表单，供用户修改信息
    u = current_user()

    update_signature_result = session.pop("update_signature_result", None)
    update_signature_success = session.pop("update_signature_success", False)

    update_password_result = session.pop("update_password_result", None)
    update_password_success = session.pop("update_password_success", False)

    update_avatar_result = session.pop("update_avatar_result", None)
    update_avatar_success = session.pop("update_avatar_success", False)

    csrf_token = make_csrf_token(u)

    return render_template('user/setting.html', u=u,
                           u_s_r=update_signature_result, u_s_s=update_signature_success,
                           u_p_r=update_password_result, u_p_s=update_password_success,
                           u_a_r=update_avatar_result, u_a_s=update_avatar_success,
                           csrf_token=csrf_token
                           )


@main.route('/update/signature', methods=['POST'])
@same_user_required
@csrf_token_required
def update_signature():
    # 保存用户签名
    form = request.form
    user_id = int(form['user_id'])
    u, result = User.update_signature(user_id, form)

    update_signature_success = u is not None
    session["update_signature_result"] = result
    session["update_signature_success"] = update_signature_success

    return redirect(url_for(".setting"))


@main.route('/update/password', methods=['POST'])
@same_user_required
@csrf_token_required
def update_password():
    # 保存密码修改
    form = request.form.to_dict()
    user_id = int(form['user_id'])

    u, result = User.update_password(user_id, form)

    update_password_success = u is not None
    session["update_password_result"] = result
    session["update_password_success"] = update_password_success

    return redirect(url_for(".setting"))


@main.route('/update/avatar', methods=['POST'])
@same_user_required
@csrf_token_required
def update_avatar():
    file = request.files['avatar']
    user_id = int(request.form['user_id'])

    u, result = User.update_avatar(user_id, file)

    update_password_success = u is not None
    session["update_avatar_result"] = result
    session["update_avatar_success"] = update_password_success
    return redirect(url_for(".setting"))
