#!/bin/bash

# The following instructions are to setup the server to run the enterprise app correctly..
# Do not alter them.

# BUILDING DATABASE

echo 'Enter your root databse username:'
read dbusername
psql -U $dbusername -d postgres -a -f model/Model.sql 


# INSTALLING DEPENDENCIES

dnf install mod_wsgi
dnf install wkhtmltopdf
pip3 install virtualenv

# COPYING PROJECT TO APACHE DIRECTORY...
cp -r enterprise /var/www/enterprise
cp /var/www/enterprise/enterprise.conf /etc/httpd/conf.d/enterprise.conf


# INSTALLING REQUIRED LIBRARIES
cd /var/www/enterprise
python3 -m venv venv
source /venv/bin/activate

pip install -r requirements.txt


# Setting up httpd permissions...
setsebool -P httpd_can_network_connect 1
setsebool -P httpd_can_network_connect_db 1
setsebool -P httpd_execmem 1
setsebool -P daemons_enable_cluster_mode 1
ausearch -c 'httpd' --raw |audit2allow -M my-httpd
semodule -X 300 -i my-httpd.pp
ausearch -c 'wkhtmltopdf' --raw | audit2allow -M my-wkhtmltopdf
semodule -X 300 -i my-wkhtmltopdf.pp
ausearch -c 'systemd' --raw | audit2allow -M my-systemd
semodule -X 300 -i my-systemd.pp