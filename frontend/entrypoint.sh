#!/bin/sh

PORT=${PORT:-8080}
echo "Setting Nginx to listen on port $PORT"
sed -i "s/listen       80;/listen       ${PORT};/" /etc/nginx/conf.d/default.conf

exec nginx -g 'daemon off;'
