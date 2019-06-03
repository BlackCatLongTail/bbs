# 换源
ln -f -s /var/www/bbs/misc/sources.list /etc/apt/sources.list
mkdir -p /root/.pip
ln -f -s /var/www/bbs/misc/pip.conf /root/.pip/pip.conf

# 装依赖
apt-get update
add-apt-repository -y ppa:deadsnakes/ppa
apt-get update
apt install -y python3.6
curl https://bootstrap.pypa.io/get-pip.py > /tmp/get-pip.py
python3.6 /tmp/get-pip.py
pip3 install jinja2 flask gunicorn PyMySQL SQLAlchemy flask-socketio gevent

# 设置登录数据库的密码
debconf-set-selections <<< 'mysql-server mysql-server/root_password password 123456'
debconf-set-selections <<< 'mysql-server mysql-server/root_password_again password 123456'
apt install -y git supervisor nginx zsh curl ufw mysql-server
sh -c "$(curl -fsSL https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"

# 配置防火墙
ufw allow 22
ufw allow 80
ufw allow 443
ufw default deny incoming
ufw default allow outgoing
ufw status verbose
ufw -f enable

# 删掉 nginx default 设置
rm -f /etc/nginx/sites-enabled/default
rm -f /etc/nginx/sites-available/default

echo 'setup_1 success'

# 装完setup_1.sh的依赖后，使用python,gunicorn,supervisor依次调试后，再装setup_2.sh来自动启动程序。