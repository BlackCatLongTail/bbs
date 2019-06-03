# 建立一个软连接
ln -s -f /var/www/bbs/bbs.conf /etc/supervisor/conf.d/bbs.conf
# 不要再 sites-available 里面放任何东西
ln -s -f /var/www/bbs/bbs.nginx /etc/nginx/sites-enabled/bbs

# 重启服务器
service supervisor restart
service nginx restart

echo 'deploy_2 success'
echo 'ip'
hostname -I