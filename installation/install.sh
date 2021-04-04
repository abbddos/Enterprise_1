#!/bin/bash

# BUILDING DATABASE:

echo 'Enter your root database username: '
read dbusername
psql -U $dbusername -d postgres -a -f ~/enterprise/model/Model.sql

# INSTALLING DEPENDENCIES...
apt install python3.9
apt install python3-pip
apt install nginx
apt install supervisor
apt install wkthmltopdf
apt install python3-venv

# INSTALLING REQUIREMENTS...
cd ~/enterprise
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# SETTING UP...
mkdir /var/log/enterprise
touch /var/log/enterprise/enterprise.err.log
touch /var/log/enterprise/enterprise.out.log
rm /etc/nginx/sites-enabled/default

cp ~/enterprise/installation/enterprise /etc/nginx/sites-enabled/enterprise
cp ~/enterprise/installation/enterprise.conf /etc/supervisor/conf.d/enterprise.conf

#run...
systemctl restart nginx
systemctl restart supervisor
