# Enterprise for warehouseing and basic accounting.
Enterprise provides a web platform for running basic warehouseing and accounting for middle sized companies that require remote and multi-user access to warehousing, accounting and invoicing records. Enterprise enables middle-sized companies to run their businesses with ease and efficiency, anywhere, anytime. 

## REQUIREMENTS
In order to run Enterprise, you will need the PostgreSQL 12 or higher, Apache webserver, and for now, a Fedora 31 or higher server. Make sure your system is up to date by running

    'sudo dnf update'

## INSTALLATION

### Installing PostgreSQL:
Please follow the steps listed in https://computingforgeeks.com/how-to-install-postgresql-12-on-fedora/ to install  and enable PostgreSQL 12 to your fedora machine. Make sure to save the root username and password you select for Postgresql somewhere you can remember so you can use them in Enterprise.

### Installing HTTPD
To install and enable httpd to your fedora machine, please follow the instructions in the following link:
https://docs.fedoraproject.org/en-US/quick-docs/getting-started-with-apache-http-server/

### Installing Enterprise
1. Getting Enterprise package from github:
gitclone https://github.com/abbddos/Enterprise_1.git

2. change to super user by running:
 'su -'
3. Navigate to where Enterprise package is downloaded to your machine.
4. Run install.sh:
 'chmod +x install.sh'
 './install.sh'

### Configure Enterprise
Before running Enterprise make sure you edit the EnterpriseConfig.py file and enter your configurations. Please make sure you have a reserved email for enterprise to send users emails from.


### Running Enterprise
Simply run httpd by:
 'systemctl start httpd'




