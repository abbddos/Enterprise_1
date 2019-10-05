#!/usr/bin/python3
import os
os.chdir('/home/abdul/enterprise/model')
MigrateCMD = 'psql -U abdul -d postgres -a -f Model.sql'
os.system(MigrateCMD)
