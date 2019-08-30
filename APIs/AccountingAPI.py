from openpyxl import load_workbook
import random
from datetime import date
import pandas as pd
from . import EnterpriseAPI

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

def GetBudgets():
    con, cur = EnterpriseAPI.root()
    cur.execute('SELECT budgetcode FROM budget')
    data = cur.fetchone()
    con.close()
    if data == None:
        return ('---',)
    else:
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

def EditCategory(sess_uname, sess_pswd, id, name, comments):
    con, cur = EnterpriseAPI.connector(sess_uname, sess_pswd)
    cur.execute('UPDATE categories SET categoryname = %s, description = %s WHERE categoryid = %s', (name, comments, id))
    con.commit()
    con.close()

def GetCurrencies():
    con, cur = EnterpriseAPI.root()
    cur.execute('SELECT CurrencyCode FROM currency')
    currencies = cur.fetchall();
    con.close()
    data = []
    for currency in currencies:
        data.append((currency[0], currency[0]))
    return data

def GetAccounts(type, category):
    con, cur = EnterpriseAPI.root()
    cur.execute('SELECT AccountCode, AccountName, Currency, openingbalance, currentbalance FROM accounts Where AccountType = %s AND AccountCategory = %s', (type, category))
    data = cur.fetchall()
    con.close()
    return data

def AddNewAccount(sess_uname, sess_pswd, account, category, code, name, currency, OBalance, CBalance, comments):
    con, cur = EnterpriseAPI.connector(sess_uname, sess_pswd)
    cur.execute('INSERT INTO accounts(accounttype, accountcategory, accountname, currency, openingbalance, currentbalance, comments, accountcode) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)', (account, category, name, currency, OBalance, CBalance, comments, code ))
    con.commit()
    con.close()