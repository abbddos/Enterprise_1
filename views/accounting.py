from flask import *
from flask_mail import *
from APIs import AccountingForms
from  APIs import AccountingAPI
from APIs import EnterpriseAPI
import pdfkit
import datetime
import app

mod = Blueprint('accounting', __name__, url_prefix = '/accounting')

@mod.route('/')
def accounting():
    data = AccountingAPI.GetCategories()
    return render_template('accounting/accounting.html', username = session['username'], role = session['role'], data = data)

@mod.route('/add_category/<category>', methods = ['GET','POST'])
def add_category(category):
    data = AccountingAPI.GetCategories()
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
    return render_template('accounting/add-category.html', username = session['username'], role = session['role'],  data = data, category = category, form = form)

@mod.route('/edit_category/<category>/<account>', methods = ['GET','POST'])
def edit_category(category, account):
    data = AccountingAPI.GetCategories()
    form = AccountingForms.Accounts(request.form)
    cats = AccountingAPI.GetCategory(session['username'], session['password'], account)
    AllAccounts = AccountingAPI.GetAccounts(category, account)
    form.Currency.choices = AccountingAPI.GetCurrencies()
    if request.method == 'POST':
        if request.form['submit'] == 'Submit':
            try:
                account = request.form['CategoryName']
                AccountingAPI.EditCategory(session['username'], session['password'],
                cats[0],
                request.form['CategoryName'],
                request.form['CategoryDescription'])
                return redirect(url_for('accounting.add_account', category = category, account = account))
            except Exception as e:
                flash(str(e), category = 'fail')
                return redirect(url_for('accounting.add_account', category = category, account = account))
    return render_template('accounting/add-account.html', username = session['username'], role = session['role'],  data = data, category = category,  cats = cats, form = form, accounts = AllAccounts, account = account)

@mod.route('/add_account/<category>/<account>', methods = ['GET','POST'])
def add_account(category, account):
    data = AccountingAPI.GetCategories()
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
    return render_template('accounting/add-account.html', username = session['username'], role = session['role'], data = data, category = category, cats = cats, form = form, accounts = AllAccounts, account = account)

@mod.route('/edit_account/<type>/<category>/<account>', methods = ['GET','POST'])
def edit_account(type, category, account):
    data = AccountingAPI.GetCategories()
    cats = AccountingAPI.GetCategory(session['username'], session['password'], category)
    currencies = AccountingAPI.GetCurrencies()
    AllAccounts = AccountingAPI.GetAccounts(type, category)
    AccountData = AccountingAPI.GetAccountData(session['username'], session['password'], type, category, account)
    if request.method == 'POST':
        if request.form['submit'] == 'Submit':
            try:
                AccountingAPI.UpdateAccount(session['username'], session['password'], request.form['AccountID'],
                type, category, 
                request.form['AccountCode'],
                request.form['AccountName'],
                request.form['Currency'],
                request.form['OpenBalance'],
                request.form['CurrentBalance'],
                request.form['Comments'])
                flash('Account successfully updated...', category = 'success')
                return redirect(url_for('accounting.add_account', category = type, account = category))
            except Exception as e:
                flash(str(e), category = 'fail')
    return render_template('accounting/edit-account.html', username = session['username'], role = session['role'], data = data, category = type,  cats = cats, accounts = AllAccounts, account = category, acdata = AccountData, curs = currencies)     

@mod.route('/journal', methods = ['GET','POST'])
def journal():
    data = AccountingAPI.GetCategories()
    jrns = AccountingAPI.GetJournals()
    FCurr = AccountingAPI.GetFuntionalCurrency()
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
    return render_template('accounting/journal.html', username = session['username'], role = session['role'], data = data,  jrns = jrns, FC = FCurr)

@mod.route('/view_journal_entry/<entrycode>', methods = ['GET','POST'])
def view_journal_entry(entrycode):
    data = AccountingAPI.GetCategories()
    jrns = AccountingAPI.GetJournals()
    data1, data2, data3 = AccountingAPI.GrabJournalEntry(entrycode)
    FCurr = AccountingAPI.GetFuntionalCurrency()
    if request.method == 'POST':
        return redirect(url_for('accounting.journal'))
    return render_template('accounting/view-journal-entry.html', username = session['username'], role = session['role'], data = data,  jrns = jrns, data1 = data1, data2 = data2, data3 = data3, FC = FCurr)

@mod.route('/currencies', methods = ['GET','POST'])
def currencies():
    data = AccountingAPI.GetCategories()
    form = AccountingForms.Currencies(request.form)
    data1 = AccountingAPI.GetAllCurrencies()
    if request.method == 'POST':
        if request.form['submit'] == 'Submit':
            try:
                NewCur = AccountingAPI.AddCurrency(session['username'], session['password'],
                request.form['CurrencyName'],
                request.form['CurrencyCode'],
                request.form['ExchageRate'],
                request.form['Functional'])
                if NewCur == False:
                    flash('Currency is successfully added', category = 'success')
                    return redirect(url_for('accounting.currencies'))
                else:
                    flash('You already have a functional currency', category = 'fail')
                    return redirect(url_for('accounting.currencies'))
            except Exception as e:
                flash(str(e), category = 'fail')
                return redirect(url_for('accounting.currencies'))
    return render_template('accounting/currencies.html', username = session['username'], role = session['role'], form = form, data = data, data1 = data1)

@mod.route('/edit_currency/<code>', methods = ['GET','POST'])
def EditCurrency(code):
    data = AccountingAPI.GetCategories()
    data1 = AccountingAPI.GetCurrency(code)
    data2 = AccountingAPI.GetAllCurrencies()
    if request.method == 'POST':
        if request.form['submit'] == 'Submit':
            try:
                UpCur = AccountingAPI.UpdateCurrency(session['username'], session['password'],
                code, 
                request.form['CurrencyName'],
                request.form['CurrencyCode'],
                request.form['ExchangeRate'],
                request.form['Functional'])
                if UpCur == False:
                    flash('Currency updated successfully...', category = 'success')
                    return redirect(url_for('accounting.currencies'))
                else:
                    flash('You already have a functional currency', category = 'fail')
                    return redirect(url_for('accounting.EditCurrency', code = code))
            except Exception as e:
                flash(str(e), category = 'fail')
                return redirect(url_for('accounting.currencies'))
    return render_template('accounting/edit_currency.html', username = session['username'], role = session['role'], data = data, data1 = data1, data2 = data2)

@mod.route('/BalanceSheet/', methods = ['GET','POST'])
def BalanceSheet():
    data = AccountingAPI.GetCategories()
    cmp = EnterpriseAPI.GetCompanyProfile()
    if request.method == 'POST':
        if request.form['submit'] == 'Submit':
            if request.form['SheetFormat'] == 'pdf':
                data1, data2 = AccountingAPI.GetBalanceSheetPDF(session['username'], session['password'], request.form['SheetDate'])
                rendered = render_template('accounting/balance_sheet.html', data1 = data1, data2 = data2, date = request.form['SheetDate'], cmp = cmp)
                pdf = pdfkit.from_string(rendered, False)
                response = make_response(pdf)
                response.headers['Content-type'] = 'application/pdf'
                response.headers['Content-Disposition'] = 'attachement; filename = balance-sheet.pdf'
                return response
            elif request.form['SheetFormat'] == 'csv':
                file = AccountingAPI.BalanceSheetCSV(session['username'], session['password'], request.form['SheetDate'])
                response = make_response(file)
                response.headers['Content-type'] = 'text/csv'
                response.headers['Content-Disposition'] = 'attachement; filename = Balance_Sheet.csv'
                return response

    return render_template('accounting/get_balancesheet.html', username = session['username'], role = session['role'], data = data)

@mod.route('/NetIncomeStatement/', methods = ['GET','POST'])
def NetINcomeStatement():
    data = AccountingAPI.GetCategories()
    cmp = EnterpriseAPI.GetCompanyProfile()
    if request.method == 'POST':
        if request.form['submit'] == 'Submit':
            if request.form['SheetFormat'] == 'pdf':
                data1, data2 = AccountingAPI.NetIncomeStatementPDF(session['username'], session['password'],
                request.form['StartDate'],
                request.form['EndDate'])
                rendered = render_template('accounting/net_income_statement.html', data1 = data1, data2 = data2, date1 = request.form['StartDate'], date2 = request.form['EndDate'], cmp = cmp)
                pdf = pdfkit.from_string(rendered, False)
                response = make_response(pdf)
                response.headers['Content-type'] = 'application/pdf'
                response.headers['Content-Disposition'] = 'attachement; filename = net_income_statement.pdf'
                return response
            elif request.form['SheetFormat'] == 'csv':
                file = AccountingAPI.NetIncomeStatementCSV(session['username'], session['password'], request.form['StartDate'], request.form['EndDate'])
                response = make_response(file)
                response.headers['Content-type'] = 'text/csv'
                response.headers['Content-Disposition'] = 'attachement; filename = Net_Income_Statement.csv'
                return response
    return render_template('accounting/get_income_statement.html', username = session['username'], role = session['role'], data = data)

@mod.route('/TrialSheet/', methods = ['GET','POST'])
def TrialSheet():
    data = AccountingAPI.GetCategories()
    data1 = AccountingAPI.GetAllAccounts()
    cmp = EnterpriseAPI.GetCompanyProfile()
    if request.method == 'POST':
        if request.form['submit'] == 'Submit':
            if request.form['SheetFormat'] == 'pdf':
                trial1, trial2 = AccountingAPI.TrialBalancePDF(session['username'],session['password'],
                request.form['StartDate'],
                request.form['EndDate'],
                request.form.getlist('act_check'))
                rendered = render_template('accounting/trial_balance_sheet.html', data = trial1, sums = trial2, date1 = request.form['StartDate'], date2 = request.form['EndDate'], cmp = cmp)
                pdf = pdfkit.from_string(rendered, False)
                response = make_response(pdf)
                response.headers['Content-type'] = 'application/pdf'
                response.headers['Content-Disposition'] = 'attachement; filename = trial_balance_statement.pdf'
                return response
            elif request.form['SheetFormat'] == 'csv':
                file = AccountingAPI.TrialBalanceCSV(session['username'],session['password'],
                request.form['StartDate'],
                request.form['EndDate'],
                request.form.getlist('act_check'))
                response = make_response(file)
                response.headers['Content-type'] = 'text/csv'
                response.headers['Content-Disposition'] = 'attachement; filename = Trial_Balance_Statement.csv'
                return response
    return render_template('accounting/get_trial_sheet.html', username = session['username'], role = session['role'], data = data, data1 = data1)

@mod.route('/ExportAccountLedger/<category>/<accountname>', methods = ['GET','POST'])
def ExportAccountLedger(category, accountname):
    if request.method == 'POST':
        if request.form['export'] == 'Export':
            try:
                if request.form['export-data'] == 'csv':
                    file = AccountingAPI.GrabAccountEntriestoCSV(accountname)
                    response = make_response(file)
                    response.headers['Content-type'] = 'text/csv'
                    response.headers['Content-Disposition'] = 'attachement; filename = {}_ledger.csv'.format(accountname)
                    return response
                elif request.form['export-data'] == 'pdf':
                    data1, data2, data3 = AccountingAPI.GrabAccountEntries(accountname)
                    rendered = render_template('accounting/Account_Ledger.html', data1 = data1, data2 = data2, data3 = data3, AccountName = accountname)
                    pdf = pdfkit.from_string(rendered, False)
                    response = make_response(pdf)
                    response.headers['Content-type'] = 'application/pdf'
                    response.headers['Content-Disposition'] = 'attachement; filename = {}_Ledger.pdf'.format(accountname)
                    return response
            except Exception as e:
                flash(str(e), category = 'fail')
                return redirect(url_for('accounting.add_account', category = category, account = accountname))
    return redirect(url_for('accounting.add_account', category = category, account = accountname))

#REST API
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

@mod.route('/GetExchange/<curr>')
def GetExchange(curr):
    data = AccountingAPI.GetExchange(str(curr).upper())
    return jsonify(ex = data[0])

@mod.route('/BringAllJournals')
def BringAllJournals():
    data = AccountingAPI.JournalsJSON()
    return jsonify(data)