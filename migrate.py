import os
import EnterpriseConfig

os.chdir('/home/abdul/enterprise/model')
MigrateCMD = 'psql -U {} -d postgres -a -f Model.sql'.format(EnterpriseConfig.dbusername)
os.system(MigrateCMD)
