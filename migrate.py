#!/usr/bin/python3
import os
import EnterpriseConfig
os.chdir('/Enterprise_1/model')
MigrateCMD = 'psql -U {} -d postgres -a -f Model.sql'.format(EnterpriseConfig.dbRoot)
os.system(MigrateCMD)
