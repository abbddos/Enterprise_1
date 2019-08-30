#!/usr/bin/python3
import os
import EnterpriseConfig
<<<<<<< HEAD
os.chdir('/Enterprise_1/model')
MigrateCMD = 'psql -U {} -d postgres -a -f Model.sql'.format(EnterpriseConfig.dbRoot)
=======

os.chdir('/home/abdul/enterprise/model')
MigrateCMD = 'psql -U {} -d postgres -a -f Model.sql'.format(EnterpriseConfig.dbusername)
>>>>>>> master
os.system(MigrateCMD)
