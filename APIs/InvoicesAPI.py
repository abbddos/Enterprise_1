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

def CreateService(sess_uname, sess_pswd, servicename, servicetype, servicecost, serviceprice, description):
    con, cur = EnterpriseAPI.connector(sess_uname, sess_pswd)
    cur.execute('SELECT CreateService(%s, %s, %s, %s, %s)', (servicename, servicetype, servicecost, serviceprice, description))
    con.commit()
    con.close()

def UpdateService(sess_uname, sess_pswd, serviceid, servicename, servicetype, servicecost, serviceprice, description):
    con, cur = EnterpriseAPI.connector(sess_uname, sess_pswd)
    cur.execute('SELECT UpdateService(%s, %s, %s, %s, %s, %s)', (serviceid, servicename, servicetype, servicecost, serviceprice, description))
    con.commit()
    con.close()

def GetAllServices():
    con, cur = EnterpriseAPI.root()
    cur.execute('SELECT * FROM Services')
    data = cur.fetchall()
    con.close()
    return data

def GetService(serviceid):
    con, cur = EnterpriseAPI.root()
    cur.execute('SELECT * FROM Services WHERE serviceid = %s', (serviceid,))
    data = cur.fetchone()
    con.close()
    return data

def GetServicesByType(servicetype):
    con, cur = EnterpriseAPI.root()
    cur.execute('SELECT * FROM Services WHERE ServiceType = %s',(servicetype,))
    data = cur.fetchall()
    con.close()
    return data

def REVSnCOST(code):
    con, cur = EnterpriseAPI.root()
    cur.execute("SELECT accountname FROM accounts WHERE accountcategory = 'Sales Revenues'")
    SR = cur.fetchall()
    cur.execute("SELECT accountname FROM accounts WHERE accountcategory = 'Cost of Goods Sold'")
    CGS = cur.fetchall()
    cur.execute('SELECT invstatus FROM invoices WHERE invoicecode = %s', (code,))
    Stat = cur.fetchone()
    con.close()
    return SR, CGS, Stat

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
    df = pd.read_sql("SELECT itemname, unit_price, unit_cost, quantity FROM packages WHERE packagecode = '{}'".format(code), con)
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
    elif type == 'return':
        code = 'RET_' + str(invdate) + '_' +  str(random.randint(100000,999999))
    elif type == 'refund':
        code = 'REF_' + str(invdate) + '_' +  str(random.randint(100000,999999))
        
    for i in range(len(desc)):
        cur.execute("INSERT INTO INVOICES(invoicetype, invoicecode, created_by, sentto, invoicedate, currency, terms, description, unitprice, quantity, lineamount, ammountsum, discount, tax, totalamount, paymentmethod, paymentaccount, comments) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
        (type, code, sess_uname, sentto, invdate, currency, term, desc[i], uniprice[i], qty[i], amnt[i], amnt_sum, discount, tax, total, pay_method, pay_acct, comments))
    con.commit()
    con.close()
    return code

def EditInvoice(sess_uname, sess_pswd, invcode, type, sentto, invdate, currency, term, desc, uniprice, qty, amnt, amnt_sum, discount, tax, total, pay_method, pay_acct, comments):
    con, cur = EnterpriseAPI.connector(sess_uname, sess_pswd)
    cur.execute('DELETE FROM invoices WHERE invoicecode = %s', (invcode,))
    for i in range(len(desc)):
        cur.execute("INSERT INTO INVOICES(invoicetype, invoicecode, created_by, sentto, invoicedate, currency, terms, description, unitprice, quantity, lineamount, ammountsum, discount, tax, totalamount, paymentmethod, paymentaccount, comments) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
        (type, invcode, sess_uname, sentto, invdate, currency, term, desc[i], uniprice[i], qty[i], amnt[i], amnt_sum, discount, tax, total, pay_method, pay_acct, comments))
    con.commit()
    con.close()

def GetInvoices(tp):
    con, cur = EnterpriseAPI.root()
    cur.execute('SELECT invoicecode, invoicedate, created_by, terms, invstatus FROM invoices WHERE invoicetype = %s GROUP BY invoicecode, invoicedate, created_by, terms, invstatus', (tp,))
    data = cur.fetchall()
    con.close()
    return data

def RegisterInvoice(invcode, sess_uname, sess_pswd, tpy,  **kwargs):
    JournalCode = 'JRN_' + str(date.today()) + '-' + str(random.randint(100000,999999))
    con, cur = EnterpriseAPI.connector(sess_uname, sess_pswd)
    if tpy == 'procurement' or tpy == 'return':
        cur.execute('SELECT RegisterInvoice_PRT(%s, %s, %s)', (JournalCode, invcode, sess_uname))
        con.commit()
        con.close()
    elif tpy == 'sales' or tpy == 'refund':
        cur.execute('SELECT RegisterInvoice_SRF(%s, %s, %s, %s, %s)', (JournalCode, invcode, sess_uname, kwargs['SR'], kwargs['CGS']))
        con.commit()
        con.close()

def UpdateInvoice(sess_uname, sess_pswd, code, tpy, status, **kwargs):
    con, cur = EnterpriseAPI.connector(sess_uname, sess_pswd)
    if tpy == 'procurement' or tpy == 'return':
        if status == 'Approved':
            cur.execute('UPDATE invoices SET invstatus = %s WHERE invoicecode = %s', (status, code))
            con.commit()
            con.close()
            RegisterInvoice(code, sess_uname, sess_pswd, tpy)
        elif status == 'Canceled':
            cur.execute('UPDATE invoices SET invstatus = %s WHERE invoicecode = %s', (status, code))
            con.commit()
            con.close()
    elif tpy == 'sales' or tpy == 'refund':
        if status == 'Approved':
            cur.execute('UPDATE invoices SET invstatus = %s WHERE invoicecode = %s', (status, code))
            con.commit()
            con.close()
            RegisterInvoice(code, sess_uname, sess_pswd, tpy, SR = kwargs['REV_Account'], CGS = kwargs['CGS_Account'])
        elif status == 'Canceled':
            cur.execute('UPDATE invoices SET invstatus = %s WHERE invoicecode = %s', (status, code))
            con.commit()
            con.close()

    

def GetPrintedInvoice(code):
    SentData = (None,)
    con, cur = EnterpriseAPI.root()
    cur.execute('SELECT invoicetype, invoicecode, created_by, sentto, invoicedate, ammountsum, discount, tax, totalamount, comments FROM invoices WHERE invoicecode = %s GROUP BY invoicetype, invoicecode, created_by, sentto, invoicedate, ammountsum, discount, tax, totalamount, comments', (code,))
    InvoiceData = cur.fetchone()

    if InvoiceData[0] == 'sales' or InvoiceData[0] == 'refund':
        cur.execute('SELECT * FROM customers WHERE name = %s', (InvoiceData[3],))
        SentData = cur.fetchone()
    elif InvoiceData[0] == 'procurement' or InvoiceData[0] == 'return':
        cur.execute('SELECT * FROM providers WHERE name = %s', (InvoiceData[3],))
        SentData = cur.fetchone()

    cur.execute('SELECT description, unitprice, quantity, lineamount, currency FROM invoices WHERE invoicecode = %s', (code,))
    ItmData = cur.fetchall()
    con.close()
    return SentData, InvoiceData, ItmData

def ApproversList():
    List = []
    con, cur = EnterpriseAPI.root()
    cur.execute("SELECT username FROM approvers WHERE can_approve = 'invoices'")
    data = cur.fetchall()
    con.close()
    for d in data:
        List.append(d[0])

    return List

def BillApproversList():
    List = []
    con, cur = EnterpriseAPI.root()
    cur.execute("SELECT username FROM approvers WHERE can_approve = 'bills'")
    data = cur.fetchall()
    con.close()
    for d in data:
        List.append(d[0])

    return List

def GetInvoice(sess_uname, sess_pswd, invcode):
    con, cur = EnterpriseAPI.connector(sess_uname, sess_pswd)
    cur.execute('SELECT sentto, invoicedate, currency, terms, ammountsum, discount, tax, totalamount, paymentmethod, paymentaccount, comments, invstatus FROM invoices WHERE invoicecode = %s GROUP BY sentto, invoicedate, currency, terms, ammountsum, discount, tax, totalamount, paymentmethod, paymentaccount, comments, invstatus',(invcode,))
    data1 = cur.fetchone()
    cur.execute('SELECT invoiceid, description, unitprice, quantity, lineamount FROM invoices WHERE invoicecode = %s', (invcode,))
    data2 = cur.fetchall()
    con.close()
    return data1, data2

def CreateBill(sess_uname, sess_pswd, billdate, tpy, acttype, actcat, actname, currency, debit, credit, description, paymethod, comments):
    code = ''
    con, cur = EnterpriseAPI.connector(sess_uname, sess_pswd)
    if tpy == 'payment':
        code = 'PAY' + '_' + str(date.today()) + str(random.randint(100000,999999))
        for i in range(len(acttype)):
            cur.execute('INSERT INTO BILLS(billcode, billdate, billtype, accounttype, accountcategory, accountname, currency, debit, credit, createdby, description) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', 
            (code, billdate, tpy, acttype[i], actcat[i], actname[i], currency[i], debit[i], paymethod['debit'], sess_uname, description[i]))
        cur.execute('INSERT INTO BILLS(billcode, billdate, billtype, accounttype, accountcategory, accountname, currency, debit, credit, createdby, comments) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
        (code, billdate, tpy, paymethod['acttype'], paymethod['actcat'], paymethod['actname'], paymethod['currency'], paymethod['debit'], paymethod['credit'], sess_uname, comments))
        con.commit()
    elif tpy == 'reception':
        code = 'REC' + '_' + str(date.today()) + str(random.randint(100000,999999))
        for i in range(len(acttype)):
            cur.execute('INSERT INTO BILLS(billcode, billdate, billtype, accounttype, accountcategory, accountname, currency, debit, credit, createdby, description) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', 
            (code, billdate, tpy, acttype[i], actcat[i], actname[i], currency[i], paymethod['credit'], credit[i], sess_uname, description[i]))
        cur.execute('INSERT INTO BILLS(billcode, billdate, billtype, accounttype, accountcategory, accountname, currency, debit, credit, createdby, comments) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
        (code, billdate, tpy, paymethod['acttype'], paymethod['actcat'], paymethod['actname'], paymethod['currency'], paymethod['debit'], paymethod['credit'], sess_uname, comments))
        con.commit()
    con.close()

def GetBills(tpy):
    con, cur = EnterpriseAPI.root()
    cur.execute('SELECT billcode, createdby, billdate, status FROM bills WHERE billtype = %s GROUP BY billcode, createdby, billdate, status', (tpy,))
    data = cur.fetchall()
    con.close()
    return data

def GetOneBill(code, tpy):
    data1 = (0,)
    data2 = (0,)
    con, cur = EnterpriseAPI.root()
    if tpy == 'payment':
        cur.execute('SELECT billcode, accountcategory, accountname, currency, billdate, credit, comments, status FROM bills WHERE billcode = %s AND billtype = %s AND credit != 0 GROUP BY billcode, accountcategory, accountname, currency, billdate, credit, comments, status', (code, tpy))
        data1 = cur.fetchone()
        cur.execute('SELECT billid, accounttype, accountcategory, accountname, currency, debit, description FROM bills WHERE billcode = %s AND billtype = %s AND debit != 0', (code, tpy))
        data2 = cur.fetchall()
    elif tpy == 'reception':
        cur.execute('SELECT billcode, accountcategory, accountname, currency, billdate, debit, comments, status FROM bills WHERE billcode = %s AND billtype = %s AND debit != 0GROUP BY billcode, accountcategory, accountname, currency, billdate, debit, comments, status', (code, tpy))
        data1 = cur.fetchone()
        cur.execute('SELECT billid, accounttype, accountcategory, accountname, currency, credit, description FROM bills WHERE billcode = %s AND billtype = %s AND credit != 0', (code, tpy))
        data2 = cur.fetchall()
    con.close()
    return data1, data2

def EditBill(sess_uname, sess_pswd, code, billdate, tpy, acttype, actcat, actname, currency, debit, credit, description, paymethod, comments):
    con, cur = EnterpriseAPI.connector(sess_uname, sess_pswd)
    cur.execute('DELETE FROM bills WHERE billcode = %s', (code,))
    if tpy == 'payment':
        for i in range(len(acttype)):
            cur.execute('INSERT INTO BILLS(billcode, billdate, billtype, accounttype, accountcategory, accountname, currency, debit, credit, createdby, description) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', 
            (code, billdate, tpy, acttype[i], actcat[i], actname[i], currency[i], debit[i], paymethod['debit'], sess_uname, description[i]))
        cur.execute('INSERT INTO BILLS(billcode, billdate, billtype, accounttype, accountcategory, accountname, currency, debit, credit, createdby, comments) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
        (code, billdate, tpy, paymethod['acttype'], paymethod['actcat'], paymethod['actname'], paymethod['currency'], paymethod['debit'], paymethod['credit'], sess_uname, comments))
        con.commit() 
    elif tpy == 'reception':
        for i in range(len(acttype)):
            cur.execute('INSERT INTO BILLS(billcode, billdate, billtype, accounttype, accountcategory, accountname, currency, debit, credit, createdby, description) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', 
            (code, billdate, tpy, acttype[i], actcat[i], actname[i], currency[i], paymethod['credit'], credit[i], sess_uname, description[i]))
        cur.execute('INSERT INTO BILLS(billcode, billdate, billtype, accounttype, accountcategory, accountname, currency, debit, credit, createdby, comments) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
        (code, billdate, tpy, paymethod['acttype'], paymethod['actcat'], paymethod['actname'], paymethod['currency'], paymethod['debit'], paymethod['credit'], sess_uname, comments))
        con.commit()
    con.close()

def RegisterBill(sess_uname, sess_pswd, billcode, status):
    con, cur = EnterpriseAPI.connector(sess_uname, sess_pswd)
    if status == 'Approved':
        cur.execute('UPDATE bills SET status = %s WHERE billcode = %s',(status, billcode))
        cur.execute('SELECT registerbill(%s)', (billcode,))
    elif status == 'Canceled':
        cur.execute('UPDATE bills SET status = %s WHERE billcode = %s',(status, billcode))
    con.commit()
    con.close()

def InvoicesReport(sess_uname, sess_pswd):
    con, cur = EnterpriseAPI.connector(sess_uname, sess_pswd)
    data = pd.read_sql('SELECT * FROM invoices ORDER BY invoicecode', con)
    file = data.to_csv()
    con.close()
    return file

def BillsReport(sess_uname, sess_pswd):
    con, cur = EnterpriseAPI.connector(sess_uname, sess_pswd)
    data = pd.read_sql('SELECT * FROM bills ORDER BY billcode', con)
    file = data.to_csv()
    con.close()
    return file