from openpyxl import load_workbook
import random
from datetime import date
import pandas as pd
from . import EnterpriseAPI

def Checker():
    data = {}
    con, cur = EnterpriseAPI.root()
    #getting assets..
    cur.execute(" SELECT SUM(currentbalance) FROM accounts WHERE accounttype = 'Assets'")
    Ast = cur.fetchone()
    #getting equities..
    cur.execute(" SELECT SUM(currentbalance) FROM accounts WHERE accounttype = 'Equities'")
    Eqt = cur.fetchone()
    #getting liabilities..
    cur.execute(" SELECT SUM(currentbalance) FROM accounts WHERE accounttype = 'Liabilities'")
    Lbt = cur.fetchone()
    #getting Expenses..
    cur.execute(" SELECT SUM(currentbalance) FROM accounts WHERE accounttype = 'Expenses'")
    Exp = cur.fetchone()
    #getting Revenues..
    cur.execute(" SELECT SUM(currentbalance) FROM accounts WHERE accounttype = 'Revenues'")
    Rev = cur.fetchone()
    #getting dividends..
    cur.execute(" SELECT SUM(currentbalance) FROM accounts WHERE accounttype = 'Dividends'")
    Dvd = cur.fetchone()
    con.close()

    if Ast[0] == None:
        Ast = 0
    else:
        Ast = float(Ast[0])
    if Eqt[0] == None:
        Eqt = 0
    else:
        Eqt = float(Eqt[0])
    if Lbt[0] == None:
        Lbt = 0
    else:
        Lbt = float(Lbt[0])
    if Exp[0] == None:
        Exp = 0
    else:
        Exp = float(Exp[0])
    if Rev[0] == None:
        Rev = 0
    else:
        Rev = float(Rev[0])
    if Dvd[0] == None:
        Dvd = 0
    else:
        Dvd = float(Dvd[0])
    
    if Ast == Eqt + Lbt + Rev - Exp - Dvd:
        data['status'] = True
    else:
        data['status'] = False
    
    return data

def GetCategories():
    Assets = []
    Equities = []
    Liabilities = []
    Revenues = []
    Expenses = []
    Dividends = []
    Cash_Check = []

    con, cur = EnterpriseAPI.root()
    cur.execute('SELECT * FROM categories')
    cats = cur.fetchall()
    con.close()

    for cat in cats:
        if cat[3] == 'Assets':
            Assets.append(cat[1])
        elif cat[3] == 'Equities':
            Equities.append(cat[1])
        elif cat[3] == 'Liabilities':
            Liabilities.append(cat[1])
        elif cat[3] == 'Revenues':
            Revenues.append(cat[1])
        elif cat[3] == 'Expenses':
            Expenses.append(cat[1])
        elif cat[3] == 'Dividends':
            Dividends.append(cat[1]) 
        elif cat[3] == 'Cash_Cehck':
            Cash_Check.append(cat[1])

    data = {'Assets': Assets, 
            'Equities': Equities,
            'Liabilities': Liabilities,
            'Revenues': Revenues,
            'Expenses': Expenses,
            'Dividends': Dividends,
            'Cash_Check': Cash_Check}

    return data

def AddCategory(sess_uname, sess_pswd, category, name, description):
    con, cur = EnterpriseAPI.connector(sess_uname, sess_pswd)
    cur.execute('INSERT INTO categories(categoryname, description, categorytype) VALUES(%s, %s, %s)',(name, description, category))
    con.commit()
    con.close()

def GetCategory(sess_uname, sess_pswd, catname):
    con, cur = EnterpriseAPI.connector(sess_uname, sess_pswd)
    cur.execute('SELECT categoryid, categoryname, description FROM categories WHERE categoryname = %s', (catname,))
    data = cur.fetchone()
    con.close()
    return data

def GrabCategory(sess_uname, sess_pswd, type):
    con, cur = EnterpriseAPI.connector(sess_uname, sess_pswd)
    cur.execute('SELECT categoryname FROM categories WHERE categorytype = %s', (type,))
    data = cur.fetchall()
    con.close()
    return data

def EditCategory(sess_uname, sess_pswd, id, name, comments):
    con, cur = EnterpriseAPI.connector(sess_uname, sess_pswd)
    cur.execute('UPDATE categories SET categoryname = %s, description = %s WHERE categoryid = %s', (name, comments, id))
    con.commit()
    con.close()

def GetCurrencies():
    con, cur = EnterpriseAPI.root()
    cur.execute('SELECT CurrencyCode FROM currency ORDER BY currencyid')
    currencies = cur.fetchall();
    con.close()
    data = []
    for currency in currencies:
        data.append((currency[0], currency[0]))
    return data

def GetAccounts(type, category):
    con, cur = EnterpriseAPI.root()
    cur.execute('SELECT AccountCode, AccountName, Currency, openingbalance, currentbalance, exchangerate FROM GetAccount Where AccountType = %s AND AccountCategory = %s', (type, category))
    data = cur.fetchall()
    con.close()
    return data

def AddNewAccount(sess_uname, sess_pswd, account, category, code, name, currency, OBalance, CBalance, comments):
    con, cur = EnterpriseAPI.connector(sess_uname, sess_pswd)
    cur.execute('SELECT CreateAccount(%s, %s, %s, %s, %s, %s, %s, %s)', (account, category, code, name, currency, OBalance, CBalance, comments))
    con.commit()
    con.close()

def GetAccountData(sess_uname, sess_pswd, type, category, account):
    con, cur = EnterpriseAPI.connector(sess_uname, sess_pswd)
    cur.execute('SELECT accountcode, accountname, currency, openingbalance, currentbalance, comments, exchangerate from GetAccount WHERE accountcode = %s', (account,))
    data = cur.fetchone()
    con.close()
    return data

def UpdateAccount(sess_uname, sess_pswd, type, category, account, name, currency, openbalance, currentbalance, comments):
    con, cur = EnterpriseAPI.connector(sess_uname, sess_pswd)
    cur.execute('SELECT UpdateAccount(%s, %s, %s, %s, %s, %s, %s, %s)',
    (type, category, account, name, currency, openbalance, currentbalance, comments))
    con.commit()
    con.close()

def GrabAccount(sess_uname, sess_pswd, cat):
    con, cur = EnterpriseAPI.connector(sess_uname, sess_pswd)
    cur.execute('SELECT accountname FROM accounts WHERE accountcategory = %s', (cat,))
    data = cur.fetchall()
    con.close()
    return data

def GrabCurrency(sess_uname, sess_pswd, act):
    con, cur = EnterpriseAPI.connector(sess_uname, sess_pswd)
    cur.execute('SELECT currency FROM accounts WHERE accountname = %s', (act,))
    data = cur.fetchall()
    con.close()
    return data

def GrabAllCurrencies(sess_uname, sess_pswd):
    con, cur = EnterpriseAPI.connector(sess_uname, sess_pswd)
    cur.execute('SELECT currencycode FROM currency')
    data = cur.fetchall()
    con.close()
    return data

def GetJournals():
    con, cur = EnterpriseAPI.root()
    cur.execute('SELECT entrycode, createdby, createdon FROM journal GROUP BY entrycode, createdby, createdon')
    data = cur.fetchall()
    con.close()
    return data

def AddJournalEntry(sess_uname, sess_pswd, acttype, actcat, actname, crncy, dbt, cdt, comments):
    JournalCode = 'JRN_' + str(date.today()) + '-' + str(random.randint(100000,999999))
    con, cur = EnterpriseAPI.connector(sess_uname, sess_pswd)
    for i in range(len(acttype)):
        if dbt[i] == '':
            dbt[i] = 0;
        elif cdt[i] == '':
            cdt[i] = 0
        cur.execute('SELECT CreateJournalEntry(%s, %s, %s, %s, %s, %s, %s, %s, %s)',
        (JournalCode, acttype[i], actcat[i], actname[i], crncy[i], dbt[i], cdt[i], sess_uname, comments[i]))
        con.commit()
    con.close()

def GrabJournalEntry(entrycode):
    con, cur = EnterpriseAPI.root()
    cur.execute('SELECT * FROM View_Journal WHERE entrycode = %s',(entrycode,))
    data1 = cur.fetchall()
    cur.execute('SELECT entrycode, createdon, createdby FROM journal WHERE entrycode = %s GROUP BY entrycode, createdon, createdby', (entrycode,))
    data2 = cur.fetchone()
    con.close()
    data3 = []
    dbt = 0
    cdt = 0
    for d in data1:
        dbt += d[6]*d[9]
        cdt += d[7]*d[9]
    data3.append(dbt)
    data3.append(cdt)
    return data1, data2, data3

def GrabAccountEntries(AccountName):
    con, cur = EnterpriseAPI.root()
    cur.execute('select entrydate, dbt, cdt, comments, forex from view_journal where accountname = %s', (AccountName,))
    data1 = cur.fetchall()
    cur.execute('select sum(dbt) as Debit, sum(cdt) as Credit, forex from view_journal where accountname  = %s group by accountname, forex', (AccountName,))
    data2 = cur.fetchone()
    cur.execute('select openingbalance, currentbalance, exchangerate from getaccount where accountname = %s', (AccountName,))
    data3 = cur.fetchone()
    con.close()
    return data1, data2, data3
    
def GetAllCurrencies():
    con, cur = EnterpriseAPI.root()
    cur.execute('SELECT * FROM currency ORDER BY currencyid')
    data = cur.fetchall()
    con.close()
    return data

def GetCurrency(id):
    con, cur = EnterpriseAPI.root()
    cur.execute('SELECT * FROM currency WHERE currencyid = %s', (id,))
    data = cur.fetchone()
    con.close()
    return data

def AddCurrency(sess_uname, sess_pswd, name, code, ex_rate, func):
    funcur = False
    con, cur = EnterpriseAPI.connector(sess_uname, sess_pswd)
    cur.execute('SELECT functionalcurrency from currency')
    data = cur.fetchall()
    for d in data:
        if func in d:
            funcur = True
    if funcur:
        con.close()
        return funcur
    else:
        cur.execute('INSERT INTO currency(currencyname, currencycode, exchangerate, functionalcurrency) VALUES(%s, %s, %s, %s)',(name, code, ex_rate, func))
        con.commit()
        return funcur
    con.close()

def UpdateCurrency(sess_uname, sess_pswd, id, name, code, ex_rate, func):
    funcur = False
    con, cur = EnterpriseAPI.connector(sess_uname, sess_pswd)
    cur.execute('SELECT functionalcurrency from currency')
    data = cur.fetchall()
    for d in data:
        if func in d:
            funcur = True
    if funcur:
        con.close()
        return funcur
    else:
        cur.execute('UPDATE currency SET CurrencyName = %s, CurrencyCode = %s, ExchangeRate = %s, FunctionalCurrency = %s WHERE CurrencyID = %s',
        (name, code, ex_rate, func, id))
        con.commit()
        return funcur
    con.close()

def GetFuntionalCurrency():
    con, cur = EnterpriseAPI.root()
    cur.execute("SELECT currencycode FROM currency WHERE functionalcurrency = 'Yes'")
    data = cur.fetchone()
    con.close()
    return data

def GetExchange(curr):
    con, cur = EnterpriseAPI.root()
    cur.execute('SELECT exchangerate FROM currency WHERE currencycode = %s', (curr,))
    data = cur.fetchone()
    con.close()
    return data

