from registry.aliyuncs.com/xiaolu-img/xiaolusys-base:forum

run mkdir -p /var/log/forum;mkdir -p /var/www/deploy/forum;mkdir -p /data/log/django;mkdir -p /data/forum/static;

add . /var/www/deploy/forum
workdir /var/www/deploy/forum/xiaoluforum

run blueware-admin generate-config BAAGUgBTVAs065dBFQpCVFgfC06fb3VaWUgEVlMFG49d7QlVGgkNH1cB843eBwBJB1RPAQI= blueware.ini

