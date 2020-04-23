from openpyxl import load_workbook
import random
from datetime import date
import pandas as pd
from . import EnterpriseAPI
import json

def CreateCustomer(sess_uname, sess_pswd, name, address, phone1, phone2, email, pobox, description):
    con, cur = EnterpriseAPI.connector(sess_uname, sess_pswd)
    cur.execute('INSERT INTO customers(name, address, phone_1, phone_2, email, pobox, description) values(%s, %s, %s, %s, %s, %s, %s)',
    (name, address, phone1, phone2, email, pobox, description))
    con.commit()
    con.close()

def UpdateCustomer(sess_uname, sess_pswd, cst, name, address, phone1, phone2, email, pobox, description):
    con, cur = EnterpriseAPI.connector(sess_uname, sess_pswd)
    cur.execute('UPDATE customers SET name = %s, address = %s, phone_1 = %s, phone_2 = %s, email = %s, pobox = %s, description = %s WHERE id = %s',
    (name, address, phone1, phone2, email, pobox, description, cst))
    con.commit()
    con.close() 

def GetAllCustomers():
    con, cur = EnterpriseAPI.root()
    cur.execute('SELECT id, name, address, phone_1, phone_2, email, pobox FROM customers')
    data = cur.fetchall()
    con.close()
    return data

def GetOneCustomer(sess_uname, sess_pswd, id):
    con, cur = EnterpriseAPI.connector(sess_uname, sess_pswd)
    cur.execute('SELECT * FROM customers WHERE id = %s', (id,))
    data = cur.fetchone()
    con.close()
    return data
