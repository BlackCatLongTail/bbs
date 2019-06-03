from flask import (
    request,
    redirect,
    url_for,
    Blueprint,
    render_template,
)

from routes import (
    current_user,
    login_required,
    csrf_token_required
)

from models.reply import Reply
from models.mail import Mail
from models.topic import Topic


main = Blueprint('reply', __name__)


def get_receivers(content):
    part = content.split(' ')
    receivers_name = []
    for p in part:
        if p.startswith('@'):
            receivers_name.append(p[1:])

    return receivers_name


def send_mails(sender, receivers_name, reply_content):
    sender_name = sender.username
    for receiver_name in receivers_name:
        d = dict(
            title='{} @ {}'.format(sender_name, receiver_name),
            content=reply_content,
            sender_id=sender.id,
            receiver_name=receiver_name
        )
        Mail.new(d)


@main.route("/add", methods=["POST"])
@login_required
def add():
    form = request.form.to_dict()
    u = current_user()

    # 如果reply中出现@，则会给对应的人发送邮件
    reply_content = form.get('content', '')
    receivers_name = get_receivers(reply_content)
    send_mails(u, receivers_name, reply_content)

    form['user_id'] = u.id
    m = Reply.new(**form)

    return redirect(url_for('topic.detail', id=m.topic_id))


@main.route("/delete")
@login_required
@csrf_token_required
def delete():
    reply_id = request.args.get('id')
    r = Reply.one(id=reply_id)
    topic_id = r.topic_id
    topic = Topic.one(id=topic_id)

    u = current_user()
    # 进行删帖权限判断：
    if u.is_admin() or u.id in [topic.user_id, r.user_id]:
        Reply.delete(reply_id)
        return redirect(url_for('topic.detail', id=topic_id))
    else:
        return render_template('no_permission.html', u=u)


