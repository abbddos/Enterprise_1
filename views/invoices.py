from flask import *
from flask_mail import *
from APIs import AccountingForms
from  APIs import AccountingAPI
from APIs import EnterForms
from  APIs import EnterpriseAPI
from  APIs import InvoicesAPI
import pdfkit
import datetime
import app

mod = Blueprint('invoices', __name__, url_prefix = '/invoices')

@mod.route('/')
def invoices():
    return render_template('invoices/invoices.html', username = session['username'])

@mod.route('/Providers/', methods = ['GET' ,'POST'])
def Providers():
    form = EnterForms.ProvidersForm(request.form)
    data = EnterpriseAPI.GetProviders()
    if request.method == 'POST':
        if request.form['submit'] == 'Submit' and form.validate():
            try:
                EnterpriseAPI.CreateProvider(session['username'], session['password'],
                request.form['name'],
                request.form['address'],
                request.form['phone1'],
                request.form['phone2'],
                request.form['email'],
                request.form['pobox'],
                request.form['description'])
                flash('Provider added Successfully', category = 'success')
                return redirect(url_for('invoices.Providers'))
            except Exception as e:
                flash(str(e), category = 'fail')
                return redirect(url_for('invoices.Providers'))
    return render_template('invoices/providers.html', username = session['username'], form = form, data = data)

@mod.route('/edit_provider/<prv>/', methods = ['GET', 'POST'])
def edit_provider(prv):
    form = EnterForms.ProvidersForm(request.form)
    data = EnterpriseAPI.GetProviders()
    data1 = EnterpriseAPI.FetchProvider(session['username'], session['password'],prv)
    if request.method == 'POST':
        if request.form['submit'] == 'Submit' and form.validate():
            try:
                EnterpriseAPI.UpdateProvider(session['username'], session['password'], prv,
                request.form['name'],
                request.form['address'],
                request.form['phone1'],
                request.form['phone2'],
                request.form['email'],
                request.form['pobox'],
                request.form['description'])
                flash('Provider updated successfully', category = 'success')
                return redirect(url_for('invoices.Providers'))
            except Exception as e:
                flash(str(e), category = 'fail')
                return redirect(url_for('invoices.Providers'))
    return render_template('invoices/edit_provider.html', username = session['username'], form = form, data = data, data1 = data1)

@mod.route('/Customers/', methods = ['GET' ,'POST'])
def Customers():
    form = EnterForms.CustomersForm(request.form)
    data = InvoicesAPI.GetAllCustomers()
    if request.method == 'POST':
        if request.form['submit'] == 'Submit' and form.validate():
            try:
                InvoicesAPI.CreateCustomer(session['username'], session['password'],
                request.form['name'],
                request.form['address'],
                request.form['phone1'],
                request.form['phone2'],
                request.form['email'],
                request.form['pobox'],
                request.form['description'])
                flash('Provider added Successfully', category = 'success')
                return redirect(url_for('invoices.Customers'))
            except Exception as e:
                flash(str(e), category = 'fail')
                return redirect(url_for('invoices.Customers'))
    return render_template('invoices/customers.html', username = session['username'], form = form, data = data)

@mod.route('/edit_customer/<cst>/', methods = ['GET', 'POST'])
def edit_customer(cst):
    form = EnterForms.CustomersForm(request.form)
    data = InvoicesAPI.GetAllCustomers()
    data1 = InvoicesAPI.GetOneCustomer(session['username'], session['password'],cst)
    if request.method == 'POST':
        if request.form['submit'] == 'Submit' and form.validate():
            try:
                InvoicesAPI.UpdateCustomer(session['username'], session['password'], cst, 
                    request.form['name'],
                    request.form['address'],
                    request.form['phone1'],
                    request.form['phone2'],
                    request.form['email'],
                    request.form['pobox'],
                    request.form['description'])
                flash('Provider updated successfully', category = 'success')
                return redirect(url_for('invoices.Customers'))
            except Exception as e:
                flash(str(e), category = 'fail')
                return redirect(url_for('invoices.Customers'))
    return render_template('invoices/edit_customer.html', username = session['username'], form = form, data = data, data1 = data1)

@mod.route('/groups/', methods = ['GET','POST'])
def groups():
    data = EnterpriseAPI.GroupList()
    if request.method == 'POST':
        if request.form['submit'] == 'Submit':
            try:
                EnterpriseAPI.AddGroup(session['username'], session['password'],
                request.form['Name'],
                request.form['description'])
                flash('Group added successfully', category = 'success')
                return redirect(url_for('invoices.groups'))
            except Exception as e:
                flash(str(e), category = 'fail')
                return redirect(url_for('invoices.groups'))
    return render_template('invoices/groups.html', username = session['username'], data = data)

@mod.route('/edit_group/<id>/', methods = ['GET','POST'])
def edit_group(id):
    data = EnterpriseAPI.GetGroup(id)
    data1 = EnterpriseAPI.GroupList()
    if request.method == 'POST':
        if request.form['submit'] == 'Submit':
            try:
                EnterpriseAPI.UpdateGroup(session['username'], session['password'], id,
                request.form['Name'],
                request.form['description'])
                flash('Group Updated Successfully', category = 'success')
                return redirect(url_for('invoices.groups'))
            except Exception as e:
                flash(str(e), category = 'fail')
                return redirect(url_for('invoices.groups'))
    return render_template('invoices/edit_group.html', data = data, data1 = data1, username = session['username'])

@mod.route('/items/', methods = ['GET','POST'])
def items():
    form = EnterForms.ItemsForm(request.form)
    data = EnterpriseAPI.GetItems()
    form.Group.choices = EnterpriseAPI.Groups()
    form.SecondaryUnit.choices = EnterpriseAPI.SecondaryUnits()
    form.Provider.choices = EnterpriseAPI.ProvidersList()
    if request.method == 'POST':
        if request.form['submit'] == 'Submit' and form.validate():
            try:
                EnterpriseAPI.CreateItem(session['username'], session['password'],
                request.form['ItemName'],
                request.form['Brand'],
                request.form['Provider'],
                request.form['Unit'],
                request.form['UnitPrice'],
                request.form['Description'],
                request.form['Size'],
                request.form['Color'],
                request.form['SKU'],
                request.form['PartNumber'],
                request.form['IEME'],
                request.form['Length'],
                request.form['Width'],
                request.form['Height'],
                request.form['Diameter'],
                request.form['LengthUnit'],
                request.form['WidthUnit'],
                request.form['HeightUnit'],
                request.form['DiamaterUnit'],
                request.form['Group'],
                request.form['Category'],
                request.form['SecondaryUnit'])
                flash('Item added successfully', category = 'success')
                return redirect(url_for('invoices.items'))
            except Exception as e:
                flash(str(e), category = 'fail')
                return redirect(url_for('invoices.items'))
    return render_template('invoices/items.html', username = session['username'], form = form, data = data)

@mod.route('/edit_item/<itm>/', methods = ['GET','POST'])
def edit_item(itm):
    data = EnterpriseAPI.GetItems()
    data1 = EnterpriseAPI.FetchItem(itm)
    provs = EnterpriseAPI.ProvidersList()
    grp = EnterpriseAPI.Groups()
    secunit = EnterpriseAPI.SecondaryUnits()
    if request.method == 'POST':
        if request.form['submit'] == 'Submit':
            try:
                EnterpriseAPI.UpdateItem(session['username'], session['password'], itm,
                request.form['ItemName'],
                request.form['Brand'],
                request.form['Provider'],
                request.form['Unit'],
                request.form['UnitPrice'],
                request.form['Description'],
                request.form['Size'],
                request.form['Color'],
                request.form['SKU'],
                request.form['PartNumber'],
                request.form['IEME'],
                request.form['Length'],
                request.form['Width'],
                request.form['Height'],
                request.form['Diameter'],
                request.form['LengthUnit'],
                request.form['WidthUnit'],
                request.form['HeightUnit'],
                request.form['DiamaterUnit'],
                request.form['Group'],
                request.form['Category'],
                request.form['SecondaryUnit'])
                flash('Item updated successfully', category = 'success')
                return redirect(url_for('invoices.items'))
            except Exception as e:
                flash(str(e), category = 'fail')
                return redirect(url_for('invoices.items'))
    return render_template('invoices/edit_item.html', username = session['username'], data = data, data1 = data1, provs = provs, grp = grp, secunit = secunit)

@mod.route('/packages/', methods = ['GET','POST'])
def packages():
    itms = EnterpriseAPI.ItemPicker()
    pkg = EnterpriseAPI.GetPackages()
    if request.method == 'POST':
        if request.form['submit'] == 'Submit':
            try:
                EnterpriseAPI.CreatePackage(session['username'], session['password'],
                request.form['packagename'],
                request.form.getlist('code'),
                request.form.getlist('Name'),
                request.form.getlist('unit'),
                request.form.getlist('quantity'),
                request.form['description'])
                flash('Package Created Successcully', category = 'success')
                return redirect(url_for('invoices.packages'))
            except Exception as e:
                i = str(request.form.getlist('unit'))
                flash(str(e), category = 'fail')
                return redirect(url_for('invoices.packages'))

    return render_template('invoices/packages.html', username = session['username'], itms = itms, pkg = pkg)

@mod.route('/edit_package/<pkg>/', methods = ['GET','POST'])
def edit_package(pkg):
    pks, itms = EnterpriseAPI.FetchPackage(pkg)
    pkk = EnterpriseAPI.GetPackages()
    itt = EnterpriseAPI.ItemPicker()
    if request.method == 'POST':
        if request.form['submit'] == 'Submit':
            try:
                EnterpriseAPI.UpdatePackage(session['username'], session['password'], pkg,
                request.form['packagename'],
                request.form.getlist('code'),
                request.form.getlist('Name'),
                request.form.getlist('unit'),
                request.form.getlist('quantity'),
                request.form['description'])
                flash('Package Updated Successfully', category = 'success')
                return redirect(url_for('invoices.packages'))
            except Exception as e:
                flash(str(e), category = 'fail')
                return redirect(url_for('invoices.packages'))
    return render_template('invoices/edit_package.html', username = session['username'], pks = pks, itms = itms, pkk = pkk, itt = itt)

@mod.route('Secondary_units/', methods = ['GET','POST'])
def SecondaryUnits():
    data = EnterpriseAPI.GetSecondaryUnits()
    if request.method == 'POST':
        if request.form['submit'] == 'Submit':
            try:
                EnterpriseAPI.CreateSecondaryUnit(session['username'], session['password'],
                request.form['secuntname'],
                request.form['secuntcode'],
                request.form['unit'],
                request.form['secuntmeasure'])
                flash('Secondary unit created successfully...', category = 'success')
                return redirect(url_for('invoices.SecondaryUnits'))
            except Exception as e:
                flash(str(e), category = 'fail')
                return redirect(url_for('invoices.SecondaryUnits'))
    return render_template('invoices/Secondary_units.html', username = session['username'], data = data)

@mod.route('Edit_Secondary_unit/<code>/', methods = ['GET','POST'])
def EditSecondaryUnit(code):
    data = EnterpriseAPI.GetSecondaryUnits()
    data1 = EnterpriseAPI.GrabSecondaryUnit(code)
    if request.method == 'POST':
        if request.form['submit'] == 'Submit':
            try:
                EnterpriseAPI.UpdateSecondaryUnit(session['username'], session['password'],
                request.form['secuntname'],
                code,
                request.form['unit'],
                request.form['secuntmeasure'])
                flash('Secondary Unit updated successfully...', category = 'success')
                return redirect(url_for('invoices.SecondaryUnits'))
            except Exception as e:
                flash(str(e), category = 'fail')
                return redirect(url_for('invoices.SecondaryUnits'))
    return render_template('invoices/Edit_secondary_unit.html', username = session['username'], data = data, data1 = data1)