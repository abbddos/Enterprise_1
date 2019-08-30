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