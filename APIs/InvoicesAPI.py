from openpyxl import load_workbook
import random
from datetime import date
import pandas as pd
from . import EnterpriseAPI
import json

def CreateCustomer(sess_uname, sess_pswd, name, address, phone1, phone2, email, pobox, description):
    con, cur = EnterpriseAPI.connector(sess_uname, sess_pswd)
    cur.execute('SELECT CreateCustomer(%s, %s, %s, %s, %s, %s, %s)',
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

def GetAccount(acc):
    con, cur = EnterpriseAPI.root()
    if acc == 'Cash':
        df = pd.read_sql("SELECT accountname FROM accounts WHERE accountcategory = 'Cash'", con)
        data = df.to_dict()
    elif acc == 'Bank transfer':
        df = pd.read_sql("SELECT accountname FROM accounts WHERE accountcategory = 'Bank Accounts'", con)
        data = df.to_dict()
    con.close()
    return data

def GetPack(code):
    con, cur = EnterpriseAPI.root()
    df = pd.read_sql("SELECT itemname, unit_price, quantity FROM packages WHERE packagecode = '{}'".format(code), con)
    data = df.transpose().to_dict()
    con.close()
    return data

def AddInvoice(sess_uname, sess_pswd, type, sentto, invdate, currency, term, desc, uniprice, qty, amnt, amnt_sum, discount, tax, total, pay_method, pay_acct, comments):
    con, cur = EnterpriseAPI.connector(sess_uname, sess_pswd)
    code = ""
    if type == 'sales':
        code = 'SALE_' + str(invdate) + '_' +  str(random.randint(100000,999999))
    elif type == 'procurement':
        code = 'PROC_' + str(invdate) + '_' +  str(random.randint(100000,999999))

    for i in range(len(desc)):
        cur.execute("INSERT INTO INVOICES(invoicetype, invoicecode, created_by, sentto, invoicedate, currency, terms, description, unitprice, quantity, lineamount, ammountsum, discount, tax, totalamount, paymentmethod, paymentaccount, comments) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
        (type, code, sess_uname, sentto, invdate, currency, term, desc[i], uniprice[i], qty[i], amnt[i], amnt_sum, discount, tax, total, pay_method, pay_acct, comments))
    con.commit()
    con.close()
    return code

def GetInvoices(tp):
    con, cur = EnterpriseAPI.root()
    cur.execute('SELECT invoicecode, invoicedate, created_by, terms FROM invoices WHERE invoicetype = %s GROUP BY invoicecode, invoicedate, created_by, terms', (tp,))
    data = cur.fetchall()
    con.close()
    return data

def RegisterInvoice(invcode, sess_uname, sess_pswd):
    JournalCode = 'JRN_' + str(date.today()) + '-' + str(random.randint(100000,999999))
    con, cur = EnterpriseAPI.connector(sess_uname, sess_pswd)
    cur.execute('SELECT RegisterInvoice(%s, %s, %s)', (JournalCode, invcode, sess_uname))
    con.commit()
    con.close()