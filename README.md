# Nterprise for warehouseing and accounting.
Nterprise is an open source web platform designed to help middle-sized businesses, where multiple users work together either on one task or on multiple integrated tasks, manage their commodities, finances, invoices and payments and produce basic reports anytime, anywhere. Because it is a multi-user web platform, Enterprise enables its users to finish tasks related to their work faster and with more efficiency, and to access tasks related information regardless the users are. 

Nterprise is mainly designed to run specifically on Linux servers as Linux has proven to be more light weight, more stable and secure and the utilization of bleeding edge technology and solutions that Linux provides, hence it is easier to maintain than other server software. Being based on Linux, Nterprise can also be considered as a more affordable solution to middle-sized businesses that have multiple users.

Though designed to mainly run on Linux servers, Nterprise can also run on Windows servers. However, Nterprise developers advise to follow the instructions listed in this documentation to install and use Nterprise. 

Nterprise developers are not currently supporting any licenses of Nterprise installed under Windows. 

## REQUIREMENTS
* In order to run Nterprise, you will need: 
    1. the latest Ubuntu or Debian based server.
    2. PostgreSQL 12 or higher, 
    3. Git  

* Make sure your server is up to date by running:
'sudo apt update && sudo apt upgrade'

* The other requirements, such as Python-3.9, nginx webserver and Supervisor will be automatically installed once you run the installation script included in Nterprise package.

## INSTALLATION

### Installing PostgreSQL:
To install postgres, please follow the instructions included in the following link:
https://technowikis.com/37107/install-postgresql-and-pgadmin4-on-ubuntu-20-10

### Installing GIT
To install Git, please run the command: 'sudo apt install git'

### Getting Nterprise
to get Nterprise package, run the following command:
gitclone https://github.com/abbddos/Enterprise_1.git enterprise

### Preinstallation configuration
Before running Nterprise make sure you do the following steps: 
* Navigate to installation directory in enterprise package,
* open the nginx configuration file 'enterprise' in the installation directory and make sure you enter your server username as per the image below:
![alt text](https://github.com/abbddos/Enterprise_1/blob/master/snapshots/nginx_conf.png)
* save and exit.
* open the Supervisor configuration file 'enterprise.conf' also included in the installation directory, and enter your server username as per the image below:
![alt text](https://github.com/abbddos/Enterprise_1/blob/master/snapshots/supervisor_conf.png)
* save and exit
* Finally, in the enterprise directory, edit the EnterpriseConfig.py file, and add the required information as per the instructions included in the file. save and exit and you are ready to install and run Nterprise.

### Installing and running Nterprise:
* Simply run the installation file included in the installation directory ./install.sh
The installer will request you to provide the root username and the password to your postgres database so it can build the Nterprise database. The installer will also automatically install all requirements and dependencies and manage the configurations.

* To run Nterprise, fetch your IP by running 'ifconfig'. copy the IP and paste it in the URL slot in any internet browser, and you're ready to use Nterprise.



