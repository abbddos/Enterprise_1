from flask import *
from flask_mail import *
from APIs import AccountingForms
from  APIs import AccountingAPI
import pdfkit
import datetime
import app

mod = Blueprint('accounting', __name__, url_prefix = '/accounting')

@mod.route('/')
def accounting():
    data = AccountingAPI.GetCategories()
    bdgts = AccountingAPI.GetBudgets()
    return render_template('accounting/accounting.html', username = session['username'], data = data, bdgts = bdgts)

@mod.route('/add_category/<category>', methods = ['GET','POST'])
def add_category(category):
    data = AccountingAPI.GetCategories()
    bdgts = AccountingAPI.GetBudgets()
    form = AccountingForms.CategoryForm(request.form)
    if request.method == 'POST':
        if request.form['submit'] == 'Submit':
            try:
                AccountingAPI.AddCategory(session['username'], session['password'],
                category,
                request.form['CategoryName'],
                request.form['CategoryDescription'])
                flash('category created successfully...', category = 'success')
                return redirect(url_for('accounting.add_category', category = category))
            except Exception as e:
                flash(str(e), category = 'fail')
                return redirect(url_for('accounting.add_category', category = category))
    return render_template('accounting/add-category.html', username = session['username'], data = data, category = category, form = form, bdgts = bdgts)

@mod.route('/edit_category/<category>/<account>', methods = ['GET','POST'])
def edit_category(category, account):
    data = AccountingAPI.GetCategories()
    bdgts = AccountingAPI.GetBudgets()
    form = AccountingForms.Accounts(request.form)
    cats = AccountingAPI.GetCategory(session['username'], session['password'], account)
    AllAccounts = AccountingAPI.GetAccounts(category, account)
    form.Currency.choices = AccountingAPI.GetCurrencies()
    if request.method == 'POST':
        if request.form['submit'] == 'Submit':
            try:
                AccountingAPI.EditCategory(session['username'], session['password'],
                cats[0],
                request.form['CategoryName'],
                request.form['CategoryDescription'])
                return redirect(url_for('accounting.add_account', category = category, account = account))
            except Exception as e:
                flash(str(e), category = 'fail')
                return redirect(url_for('accounting.add_account', category = category, account = account))
    return render_template('accounting/add-account.html', username = session['username'], data = data, category = category, bdgts = bdgts, cats = cats, form = form, accounts = AllAccounts, account = account)

@mod.route('/add_account/<category>/<account>', methods = ['GET','POST'])
def add_account(category, account):
    data = AccountingAPI.GetCategories()
    bdgts = AccountingAPI.GetBudgets()
    form = AccountingForms.Accounts(request.form)
    cats = AccountingAPI.GetCategory(session['username'], session['password'], account)
    AllAccounts = AccountingAPI.GetAccounts(category, account)
    form.Currency.choices = AccountingAPI.GetCurrencies()
    if request.method == 'POST':
        if request.form['submit'] == 'Submit':
            try:
                AccountingAPI.AddNewAccount(session['username'], session['password'],
                category, account, 
                request.form['AccountCode'],
                request.form['AccountName'],
                request.form['Currency'],
                request.form['OpeningBalance'],
                request.form['CurrentBalance'],
                request.form['Comments'])
                flash('Account Created', category = 'success')
                return redirect(url_for('accounting.add_account', category = category, account = account))
            except Exception as e:
                flash(str(e), category = 'fail')
                return redirect(url_for('accounting.add_account', category = category, account = account))
    return render_template('accounting/add-account.html', username = session['username'], data = data, category = category, bdgts = bdgts, cats = cats, form = form, accounts = AllAccounts, account = account)

@mod.route('/edit_account/<type>/<category>/<account>', methods = ['GET','POST'])
def edit_account(type, category, account):
    data = AccountingAPI.GetCategories()
    bdgts = AccountingAPI.GetBudgets()
    cats = AccountingAPI.GetCategory(session['username'], session['password'], account)
    currencies = AccountingAPI.GetCurrencies()
    AllAccounts = AccountingAPI.GetAccounts(type, category)
    AccountData = AccountingAPI.GetAccountData(session['username'], session['password'], type, category, account)
    if request.method == 'POST':
        if request.form['submit'] == 'Submit':
            try:
                AccountingAPI.UpdateAccount(session['username'], session['password'],
                type, category, account, 
                request.form['AccountName'],
                request.form['Currency'],
                request.form['OpenBalance'],
                request.form['CurrentBalance'],
                request.form['Comments'])
                flash('Account successfully updated...', category = 'success')
                return redirect(url_for('accounting.add_account', category = type, account = category))
            except Exception as e:
                flash(str(e), category = 'fail')
    return render_template('accounting/edit-account.html', username = session['username'], data = data, category = type, bdgts = bdgts, cats = cats, accounts = AllAccounts, account = category, acdata = AccountData, curs = currencies)     

@mod.route('/journal', methods = ['GET','POST'])
def journal():
    data = AccountingAPI.GetCategories()
    bdgts = AccountingAPI.GetBudgets()
    jrns = AccountingAPI.GetJournals()
    if request.method == 'POST':
        if request.form['submit'] == 'Submit':
            try:
                AccountingAPI.AddJournalEntry(session['username'], session['password'],
                request.form.getlist('account-type'),
                request.form.getlist('account-category'),
                request.form.getlist('account-name'),
                request.form.getlist('currency'),
                request.form.getlist('debit'),
                request.form.getlist('credit'),
                request.form.getlist('comments'))
                flash('Journal successfully created...', category = 'success')
                return redirect(url_for('accounting.journal'))
            except Exception as e:
                flash(str(e), category = 'fail')
                return redirect(url_for('accounting.journal'))
    return render_template('accounting/journal.html', username = session['username'], data = data, bdgts = bdgts, jrns = jrns)

@mod.route('/view_journal_entry/<entrycode>', methods = ['GET','POST'])
def view_journal_entry(entrycode):
    data = AccountingAPI.GetCategories()
    bdgts = AccountingAPI.GetBudgets()
    jrns = AccountingAPI.GetJournals()
    data1, data2, data3 = AccountingAPI.GrabJournalEntry(entrycode)
    if request.method == 'POST':
        return redirect(url_for('accounting.journal'))
    return render_template('accounting/view-journal-entry.html', username = session['username'], data = data, bdgts = bdgts, jrns = jrns, data1 = data1, data2 = data2, data3 = data3)

@mod.route('/currencies', methods = ['GET','POST'])
def currencies():
    form = AccountingForms.Currencies(request.form)
    data = AccountingAPI.GetAllCurrencies()
    if request.method == 'POST':
        if request.form['submit'] == 'Submit':
            try:
                AccountingAPI.AddCurrency(session['username'], session['password'],
                request.form['CurrencyName'],
                request.form['CurrencyCode'],
                request.form['ExchageRate'],
                request.form['Functional'])
                flash('Currency is successfully added', category = 'success')
                return redirect(url_for('accounting.currencies'))
            except Exception as e:
                flash(str(e), category = 'fail')
                return redirect(url_for('accounting.currencies'))
    return render_template('accounting/currencies.html', username = session['username'], form = form, data = data)

@mod.route('/edit_currency/<code>', methods = ['GET','POST'])
def EditCurrency(code):
    data = AccountingAPI.GetCurrency(code)
    data1 = AccountingAPI.GetAllCurrencies()
    if request.method == 'POST':
        if request.form['submit'] == 'Submit':
            try:
                AccountingAPI.UpdateCurrency(session['username'], session['password'],
                code, 
                request.form['CurrencyName'],
                request.form['CurrencyCode'],
                request.form['ExchangeRate'],
                request.form['Functional'])
                flash('Currency updated successfully...', category = 'success')
                return redirect(url_for('accounting.currencies'))
            except Exception as e:
                flash(str(e), category = 'fail')
                return redirect(url_for('accounting.currencies'))
    return render_template('accounting/edit_currency.html', username = session['username'], data = data, data1 = data1)

#JSON returning urls...
@mod.route('/checker/')
def checker():
    data = AccountingAPI.Checker()
    return jsonify(data)

@mod.route('/GrabCategory/<type>')
def GrabCategory(type):
    cats = AccountingAPI.GrabCategory(session['username'], session['password'], type)
    cat = []
    for c in cats:
        cat.append(c[0])
    return jsonify(cat = cat)

@mod.route('/GrabActName/<cat>')
def GrabActName(cat):
    acts = AccountingAPI.GrabAccount(session['username'], session['password'], cat)
    act = []
    for a in acts:
        act.append(a[0])
    return jsonify(act = act)

@mod.route('/GrabCurrency/<act>')
def GrabCurrency(act):
    curs = AccountingAPI.GrabCurrency(session['username'], session['password'], act)
    cur = []
    for c in curs:
        cur.append(c[0])
    return jsonify(cur = cur)

@mod.route('/GrabJournalEntry/<entrycode>')
def GranJournalEntry(entrycode):
    data = AccountingAPI.GrabJournalEntry(entrycode)
    return jsonify([{'Account-type': d[0], 'Account-Category': d[1], 'Account-Name': d[2], 'Currency':d[3], 'Debit': d[4], 'Credit':d[5], 'Comments':d[6]} for d in data])

@mod.route('/GrabAccountEntries/<AccountName>')
def GrabAccountEntries(AccountName):
    data1, data2, data3 = AccountingAPI.GrabAccountEntries(AccountName)
    return jsonify(info = data1, totals = data2, balances = data3)

@mod.route('/GrabAllCurrencies/')
def GrabAllCurrencies():
    data = AccountingAPI.GrabAllCurrencies(session['username'], session['password'])
    return jsonify( cur = data)