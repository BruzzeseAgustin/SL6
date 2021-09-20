
#!/bin/bash

service postgresql initdb
service postgresql start

# /etc/init.d/globus-gridftp-server start > /var/log/griftp-server.log

echo "" | sudo service mysqld start
echo 'CREATE DATABASE magic;' | mysql -u root

./renew_proxy.sh &

echo "[include]
files = /etc/supervisord.d/*.conf

[program:gridftp-server]
command=/etc/init.d/globus-gridftp-server start
startsecs=0
stopwaitsecs=10
user=root 
redirect_stderr=true
redirect stdout=true
stdout_logfile=/var/log/gridftp-server
autostart=false

[program:mysql-add-transfer]
command=mysql -u root magic < /mysql-data/TRANSFER.sql
startsecs=0
stopwaitsecs=10
user=root
redirect_stderr=true
redirect stdout=true
stdout_logfile=/var/mysql-add-transfer.log
autostart=true

[program:mysql-add-storage]
command=mysql -u root magic < /mysql-data/STORAGE.sql
startsecs=0
stopwaitsecs=10
user=root
redirect_stderr=true
redirect stdout=true
stdout_logfile=/var/mysql-add-storage.log
autostart=true" >> /etc/supervisord.conf

/usr/bin/supervisord -c /etc/supervisord.conf -n &

supervisorctl start gridftp-server

su mysql -c "mysql -u root magic < /mysql-data/TRANSFER.sql"
echo "Finished restore of the transfer mysql db" >> /var/log/mysql-add-transfer.log
su mysql -c "mysql -u root magic < /mysql-data/STORAGE.sql" 
echo "Finished restore of the storage mysql db" >> /var/log/mysql-add-storage.log

# keep container running
tail -f /dev/null

