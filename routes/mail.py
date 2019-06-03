from flask import (
    request,
    redirect,
    url_for,
    Blueprint,
    render_template,
    session,
)

from routes import (
    current_user,
    login_required,
    csrf_token_required,
    make_csrf_token
)

from models.mail import Mail
from models.user import User


main = Blueprint('mail', __name__)


@main.route("/index")
@login_required
def index():
    send_mail_result = session.pop('send_mail_result', None)
    send_mail_success = session.pop('send_mail_success', False)

    u = current_user()
    send_mails = Mail.all(sender_id=u.id)
    receive_mails = Mail.all(receiver_id=u.id)
    csrf_token = make_csrf_token(u)
    return render_template('mail/index.html',
                           u=u,
                           send_mails=send_mails,
                           receive_mails=receive_mails,
                           csrf_token=csrf_token,
                           s_m_r=send_mail_result,
                           s_m_s=send_mail_success
                           )


@main.route("/add", methods=["POST"])
@login_required
@csrf_token_required
def add():
    form = request.form.to_dict()
    u = current_user()
    form['sender_id'] = u.id
    m, result = Mail.new(form)

    send_mail_success = m is not None
    session['send_mail_result'] = result
    session['send_mail_success'] = send_mail_success

    return redirect(url_for('.index'))


@main.route("/detail")
@login_required
def detail():
    m_id = request.args.get('id')
    m = Mail.one(id=m_id)
    u = current_user()
    # 只有发件人或者收件人才有权限查看邮件
    if u.id in [m.sender_id, m.receiver_id]:
        return render_template('mail/detail.html', u=u, m=m, User=User)
    else:
        return render_template('no_permission.html', u=u)
