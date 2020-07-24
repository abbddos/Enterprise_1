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
                request.form['UnitCost'],
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
                request.form['UnitCost'],
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
                request.form.getlist('unitprice'),
                request.form.getlist('unitcost'),
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
                request.form.getlist('unitprice'),
                request.form.getlist('unitcost'),
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

@mod.route('sales_invoice/', methods = ['GET','POST'])
def SalesInvoice():
    customers = InvoicesAPI.GetAllCustomers()
    currencies = AccountingAPI.GetAllCurrencies()
    itms = EnterpriseAPI.ItemPicker()
    pkgs = EnterpriseAPI.PackagePicker()
    invs = InvoicesAPI.GetInvoices('sales')
    if request.method == 'POST':
        if request.form['submit'] == 'Submit':
            try:
                invcode = InvoicesAPI.AddInvoice(session['username'], session['password'], 'sales',
                request.form['Customer'],
                request.form['SheetDate'],
                request.form['currency'],
                request.form['terms'],
                request.form.getlist('description'),
                request.form.getlist('unitprice'),
                request.form.getlist('quantity'),
                request.form.getlist('amount'),
                request.form['totalamount'],
                request.form['discount'],
                request.form['tax'],
                request.form['invamount'],
                request.form['pay_method'],
                request.form['billing_account'],
                request.form['comments']
                )
                
                flash('Invoices created successfully', category = 'success')
                return redirect(url_for('invoices.SalesInvoice'))
            except Exception as e:
                flash(str(e), category = 'fail')
                return redirect(url_for('invoices.SalesInvoice'))
    return render_template('invoices/sales_invoice.html', username = session['username'], itms = itms, pkgs = pkgs, customers = customers, currencies = currencies, invs = invs)

@mod.route('edit_sales_invoice/<invcode>', methods = ['GET','POST'])
def EditSalesInvoice(invcode):
    customers = InvoicesAPI.GetAllCustomers()
    currencies = AccountingAPI.GetAllCurrencies()
    itms = EnterpriseAPI.ItemPicker()
    pkgs = EnterpriseAPI.PackagePicker()
    invs = InvoicesAPI.GetInvoices('sales')
    data1, data2 = InvoicesAPI.GetInvoice(session['username'], session['password'], invcode)
    if request.method == 'POST':
        if request.form['submit'] == 'Submit':
            try:
                InvoicesAPI.EditInvoice(session['username'], session['password'], invcode, 'sales',
                request.form['Customer'],
                request.form['SheetDate'],
                request.form['currency'],
                request.form['terms'],
                request.form.getlist('description'),
                request.form.getlist('unitprice'),
                request.form.getlist('quantity'),
                request.form.getlist('amount'),
                request.form['totalamount'],
                request.form['discount'],
                request.form['tax'],
                request.form['invamount'],
                request.form['pay_method'],
                request.form['billing_account'],
                request.form['comments']
                )
                
                flash('Invoices updated successfully', category = 'success')
                return redirect(url_for('invoices.SalesInvoice')) 
            except Exception as e:
                flash(str(e), category = 'fail')
                return redirect(url_for('invoices.SalesInvoice')) 
    return render_template('invoices/edit_sales_invoice.html', username = session['username'], itms = itms, pkgs = pkgs, customers = customers, currencies = currencies, invs = invs, data1 = data1, data2 = data2, invcode = invcode)


@mod.route('procurement_invoice/', methods = ['GET','POST'])
def ProcurementInvoice():
    providers = EnterpriseAPI.GetProviders()
    currencies = AccountingAPI.GetAllCurrencies()
    itms = EnterpriseAPI.ItemPicker()
    pkgs = EnterpriseAPI.PackagePicker()
    invs = InvoicesAPI.GetInvoices('procurement')
    if request.method == 'POST':
        if request.form['submit'] == 'Submit':
            try:
                invcode = InvoicesAPI.AddInvoice(session['username'], session['password'], 'procurement',
                request.form['Customer'],
                request.form['SheetDate'],
                request.form['currency'],
                request.form['terms'],
                request.form.getlist('description'),
                request.form.getlist('unitprice'),
                request.form.getlist('quantity'),
                request.form.getlist('amount'),
                request.form['totalamount'],
                request.form['discount'],
                request.form['tax'],
                request.form['invamount'],
                request.form['pay_method'],
                request.form['billing_account'],
                request.form['comments']
                )
                
                flash('Invoices created successfully', category = 'success')
                return redirect(url_for('invoices.ProcurementInvoice'))
            except Exception as e:
                flash(str(e), category = 'fail')
                return redirect(url_for('invoices.ProcurementInvoice'))
    return render_template('invoices/procurement_invoice.html', username = session['username'], itms = itms, pkgs = pkgs, providers = providers, currencies = currencies, invs = invs)

@mod.route('edit_procurement_invoice/<invcode>', methods = ['GET','POST'])
def EditProcurementInvoice(invcode):
    providers = EnterpriseAPI.GetProviders()
    currencies = AccountingAPI.GetAllCurrencies()
    itms = EnterpriseAPI.ItemPicker()
    pkgs = EnterpriseAPI.PackagePicker()
    invs = InvoicesAPI.GetInvoices('procurement')
    data1, data2 = InvoicesAPI.GetInvoice(session['username'], session['password'], invcode)
    if request.method == 'POST':
        if request.form['submit'] == 'Submit':
            try:
                InvoicesAPI.EditInvoice(session['username'], session['password'], invcode, 'procurement',
                request.form['Customer'],
                request.form['SheetDate'],
                request.form['currency'],
                request.form['terms'],
                request.form.getlist('description'),
                request.form.getlist('unitprice'),
                request.form.getlist('quantity'),
                request.form.getlist('amount'),
                request.form['totalamount'],
                request.form['discount'],
                request.form['tax'],
                request.form['invamount'],
                request.form['pay_method'],
                request.form['billing_account'],
                request.form['comments']
                )
                
                flash('Invoices updated successfully', category = 'success')
                return redirect(url_for('invoices.ProcurementInvoice')) 
            except Exception as e:
                flash(str(e), category = 'fail')
                return redirect(url_for('invoices.ProcurementInvoice')) 
    return render_template('invoices/edit_procurement_invoice.html', username = session['username'], itms = itms, pkgs = pkgs, providers = providers, currencies = currencies, invs = invs, data1 = data1, data2 = data2, invcode = invcode)

@mod.route('return_invoice/', methods = ['GET','POST'])
def ReturnInvoice():
    providers = EnterpriseAPI.GetProviders()
    currencies = AccountingAPI.GetAllCurrencies()
    itms = EnterpriseAPI.ItemPicker()
    pkgs = EnterpriseAPI.PackagePicker()
    invs = InvoicesAPI.GetInvoices('return')
    if request.method == 'POST':
        if request.form['submit'] == 'Submit':
            try:
                invcode = InvoicesAPI.AddInvoice(session['username'], session['password'], 'return',
                request.form['Customer'],
                request.form['SheetDate'],
                request.form['currency'],
                request.form['terms'],
                request.form.getlist('description'),
                request.form.getlist('unitprice'),
                request.form.getlist('quantity'),
                request.form.getlist('amount'),
                request.form['totalamount'],
                request.form['discount'],
                request.form['tax'],
                request.form['invamount'],
                request.form['pay_method'],
                request.form['billing_account'],
                request.form['comments']
                )
                
                flash('Invoices created successfully', category = 'success')
                return redirect(url_for('invoices.ReturnInvoice'))
            except Exception as e:
                flash(str(e), category = 'fail')
                return redirect(url_for('invoices.ReturnInvoice'))
    return render_template('invoices/return_invoice.html', username = session['username'], itms = itms, pkgs = pkgs, providers = providers, currencies = currencies, invs = invs)

@mod.route('edit_return_invoice/<invcode>', methods = ['GET','POST'])
def EditReturnInvoice(invcode):
    providers = EnterpriseAPI.GetProviders()
    currencies = AccountingAPI.GetAllCurrencies()
    itms = EnterpriseAPI.ItemPicker()
    pkgs = EnterpriseAPI.PackagePicker()
    invs = InvoicesAPI.GetInvoices('return')
    data1, data2 = InvoicesAPI.GetInvoice(session['username'], session['password'], invcode)
    if request.method == 'POST':
        if request.form['submit'] == 'Submit':
            try:
                InvoicesAPI.EditInvoice(session['username'], session['password'], invcode, 'return',
                request.form['Customer'],
                request.form['SheetDate'],
                request.form['currency'],
                request.form['terms'],
                request.form.getlist('description'),
                request.form.getlist('unitprice'),
                request.form.getlist('quantity'),
                request.form.getlist('amount'),
                request.form['totalamount'],
                request.form['discount'],
                request.form['tax'],
                request.form['invamount'],
                request.form['pay_method'],
                request.form['billing_account'],
                request.form['comments']
                )
                
                flash('Invoices updated successfully', category = 'success')
                return redirect(url_for('invoices.ReturnInvoice')) 
            except Exception as e:
                flash(str(e), category = 'fail')
                return redirect(url_for('invoices.ReturnInvoice')) 
    return render_template('invoices/edit_return_invoice.html', username = session['username'], itms = itms, pkgs = pkgs, providers = providers, currencies = currencies, invs = invs, data1 = data1, data2 = data2, invcode = invcode)

@mod.route('refund_invoice/', methods = ['GET','POST'])
def RefundInvoice():
    customers = InvoicesAPI.GetAllCustomers()
    currencies = AccountingAPI.GetAllCurrencies()
    itms = EnterpriseAPI.ItemPicker()
    pkgs = EnterpriseAPI.PackagePicker()
    invs = InvoicesAPI.GetInvoices('refund')
    if request.method == 'POST':
        if request.form['submit'] == 'Submit':
            try:
                invcode = InvoicesAPI.AddInvoice(session['username'], session['password'], 'refund',
                request.form['Customer'],
                request.form['SheetDate'],
                request.form['currency'],
                request.form['terms'],
                request.form.getlist('description'),
                request.form.getlist('unitprice'),
                request.form.getlist('quantity'),
                request.form.getlist('amount'),
                request.form['totalamount'],
                request.form['discount'],
                request.form['tax'],
                request.form['invamount'],
                request.form['pay_method'],
                request.form['billing_account'],
                request.form['comments']
                )
                
                flash('Invoices created successfully', category = 'success')
                return redirect(url_for('invoices.RefundInvoice'))
            except Exception as e:
                flash(str(e), category = 'fail')
                return redirect(url_for('invoices.RefundInvoice'))
    return render_template('invoices/refund_invoice.html', username = session['username'], itms = itms, pkgs = pkgs, customers = customers, currencies = currencies, invs = invs)

@mod.route('edit_refund_invoice/<invcode>', methods = ['GET','POST'])
def EditRefundInvoice(invcode):
    customers = InvoicesAPI.GetAllCustomers()
    currencies = AccountingAPI.GetAllCurrencies()
    itms = EnterpriseAPI.ItemPicker()
    pkgs = EnterpriseAPI.PackagePicker()
    invs = InvoicesAPI.GetInvoices('refund')
    data1, data2 = InvoicesAPI.GetInvoice(session['username'], session['password'], invcode)
    if request.method == 'POST':
        if request.form['submit'] == 'Submit':
            try:
                InvoicesAPI.EditInvoice(session['username'], session['password'], invcode, 'refund',
                request.form['Customer'],
                request.form['SheetDate'],
                request.form['currency'],
                request.form['terms'],
                request.form.getlist('description'),
                request.form.getlist('unitprice'),
                request.form.getlist('quantity'),
                request.form.getlist('amount'),
                request.form['totalamount'],
                request.form['discount'],
                request.form['tax'],
                request.form['invamount'],
                request.form['pay_method'],
                request.form['billing_account'],
                request.form['comments']
                )
                
                flash('Invoices updated successfully', category = 'success')
                return redirect(url_for('invoices.RefundInvoice')) 
            except Exception as e:
                flash(str(e), category = 'fail')
                return redirect(url_for('invoices.RefundInvoice')) 
    return render_template('invoices/edit_refund_invoice.html', username = session['username'], itms = itms, pkgs = pkgs, customers = customers, currencies = currencies, invs = invs, data1 = data1, data2 = data2, invcode = invcode)




@mod.route('print_invoice/<code>')
def PrintInvoice(code):
    SentData, InvoiceData, ItmData = InvoicesAPI.GetPrintedInvoice(code)
    rendered = render_template('invoices/printed_invoice.html', SentData = SentData, InvoiceData = InvoiceData, ItmData = ItmData)
    pdf = pdfkit.from_string(rendered, False)
    response = make_response(pdf)
    response.headers['Content-type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachement; filename = invoice.pdf'
    return response

@mod.route('invoice_view/<code>')
def InvoiceView(code):
    SentData, InvoiceData, ItmData = InvoicesAPI.GetPrintedInvoice(code)
    return render_template('invoices/printed_invoice.html', SentData = SentData, InvoiceData = InvoiceData, ItmData = ItmData)


@mod.route('view_invoice/<code>/<tpy>', methods = ['GET','POST'])
def ViewInvoice(code, tpy):
    Appr = InvoicesAPI.ApproversList()
    iframe = url_for('invoices.InvoiceView', code = code)
    invs = InvoicesAPI.GetInvoices(tpy)
    RS, CGS, Stat = InvoicesAPI.REVSnCOST(code)
    if request.method == 'POST':
        if request.form['submit'] == 'Submit' and session['username'] in Appr:
            if tpy == 'procurement' or tpy == 'return':
                try:
                    InvoicesAPI.UpdateInvoice(session['username'], session['password'], code, tpy, request.form['statuses'])
                    flash('Invoice updated successfully...', category = 'success')
                    return redirect(url_for('invoices.ViewInvoice', code = code, tpy = tpy))
                except Exception as e:
                    flash(str(e), category = 'fail')
                    return redirect(url_for('invoices.ViewInvoice', code = code, tpy = tpy))
            elif tpy == 'sales' or tpy == 'refund':
                try:
                    InvoicesAPI.UpdateInvoice(session['username'], session['password'], code, tpy, request.form['statuses'], 
                    REV_Account = request.form['RVACT'], CGS_Account = request.form['CGSACT'])
                    flash('Invoice updated successfully...', category = 'success')
                    return redirect(url_for('invoices.ViewInvoice', code = code, tpy = tpy))
                except Exception as e:
                    flash(str(e), category = 'fail')
                    return redirect(url_for('invoices.ViewInvoice', code = code, tpy = tpy))
        else:
            flash('User does not have permission to approve or cancel this invoice', category = 'fail')
            return redirect(url_for('invoices.ViewInvoice', code = code, tpy = tpy))
    return render_template('invoices/view_invoice.html', username = session['username'], invs = invs, iframe = iframe, type = tpy, RS = RS, CGS = CGS, Stat = Stat)

@mod.route('payment_bill/', methods = ['GET','POST'])
def PaymentBill():
    bills = InvoicesAPI.GetBills('payment')
    paymethod = {}
    if request.method == 'POST':
        if request.form['submit'] == 'Submit':
            try:
                paymethod['acttype'] = 'Assets'
                paymethod['actcat'] = request.form['PaymentMethod']
                paymethod['actname'] = request.form['PaymentAccount']
                paymethod['currency'] = request.form['PaymentCurrency']
                paymethod['debit'] = 0
                paymethod['credit'] = request.form['credit']

                InvoicesAPI.CreateBill(session['username'], session['password'],
                request.form['PaymentDate'], 'payment',
                request.form.getlist('account-type'),
                request.form.getlist('account-category'),
                request.form.getlist('account-name'),
                request.form.getlist('currency'),
                request.form.getlist('debit'),
                paymethod['debit'],
                request.form.getlist('description'),
                paymethod,
                request.form['comments']
                ) 
                flash('Bill successfully created...', category = 'success')
                return redirect(url_for('invoices.PaymentBill'))
            except Exception as e:
                flash(str(e), category = 'fail')
                return redirect(url_for('invoices.PaymentBill'))
    return render_template('invoices/payment_bill.html', username = session['username'], bills = bills)

@mod.route('edit_payment_bill/<billcode>', methods = ['GET','POST'])
def EditPaymentBill(billcode):
    bills = InvoicesAPI.GetBills('payment')
    paymethod = {}
    data1, data2 = InvoicesAPI.GetOneBill(billcode, 'payment')
    if request.method == 'POST':
        if request.form['submit'] == 'Submit':
            try:
                paymethod['acttype'] = 'Assets'
                paymethod['actcat'] = request.form['PaymentMethod']
                paymethod['actname'] = request.form['PaymentAccount']
                paymethod['currency'] = request.form['PaymentCurrency']
                paymethod['debit'] = 0
                paymethod['credit'] = request.form['credit']

                InvoicesAPI.EditBill(session['username'], session['password'], billcode,
                request.form['PaymentDate'], 'payment',
                request.form.getlist('account-type'),
                request.form.getlist('account-category'),
                request.form.getlist('account-name'),
                request.form.getlist('currency'),
                request.form.getlist('debit'),
                paymethod['debit'],
                request.form.getlist('description'),
                paymethod,
                request.form['comments']
                ) 
                flash('Bill successfully created...', category = 'success')
                return redirect(url_for('invoices.PaymentBill'))
            except Exception as e:
                flash(str(e), category = 'fail')
                return redirect(url_for('invoices.PaymentBill'))
    return render_template('invoices/edit_payment_bill.html', username = session['username'], 
    bills = bills,
    data1 = data1,
    data2 = data2)

@mod.route('view_payment_bill/<billcode>', methods = ['GET','POST'])
def ViewPaymentBill(billcode):
    Appr = InvoicesAPI.BillApproversList()
    bills = InvoicesAPI.GetBills('payment')
    paymethod = {}
    data1, data2 = InvoicesAPI.GetOneBill(billcode, 'payment')
    if request.method == 'POST':
        if request.form['submit'] == 'Submit'and session['username'] in Appr:
            try:
                InvoicesAPI.RegisterBill(session['username'], session['password'], billcode, request.form['status'])
                flash('Bill registered successfully...', category = 'success')
                return redirect(url_for('invoices.PaymentBill'))
            except Exception as e:
                flash(str(e), category = 'fail')
                return redirect(url_for('invoices.PaymentBill'))
        else:
            flash('This user does not have permission to register this bill...', category = 'fail')
            return redirect(url_for('invoices.ViewPaymentBill', billcode = billcode))
    return render_template('invoices/view_payment_bill.html', username = session['username'], 
    bills = bills,
    data1 = data1,
    data2 = data2)

@mod.route('reception_bill/', methods = ['GET','POST'])
def ReceptionBill():
    bills = InvoicesAPI.GetBills('reception')
    paymethod = {}
    if request.method == 'POST':
        if request.form['submit'] == 'Submit':
            try:
                paymethod['acttype'] = 'Assets'
                paymethod['actcat'] = request.form['PaymentMethod']
                paymethod['actname'] = request.form['PaymentAccount']
                paymethod['currency'] = request.form['PaymentCurrency']
                paymethod['debit'] = request.form['debit']
                paymethod['credit'] = 0

                InvoicesAPI.CreateBill(session['username'], session['password'],
                request.form['PaymentDate'], 'reception',
                request.form.getlist('account-type'),
                request.form.getlist('account-category'),
                request.form.getlist('account-name'),
                request.form.getlist('currency'),
                paymethod['credit'],
                request.form.getlist('credit'),
                request.form.getlist('description'),
                paymethod,
                request.form['comments']
                ) 
                flash('Bill successfully created...', category = 'success')
                return redirect(url_for('invoices.ReceptionBill'))
            except Exception as e:
                flash(str(e), category = 'fail')
                return redirect(url_for('invoices.ReceptionBill'))
    return render_template('invoices/reception_bill.html', username = session['username'], bills = bills)

@mod.route('edit_reception_bill/<billcode>', methods = ['GET','POST'])
def EditReceptionBill(billcode):
    bills = InvoicesAPI.GetBills('reception')
    paymethod = {}
    data1, data2 = InvoicesAPI.GetOneBill(billcode, 'reception')
    if request.method == 'POST':
        if request.form['submit'] == 'Submit':
            try:
                paymethod['acttype'] = 'Assets'
                paymethod['actcat'] = request.form['PaymentMethod']
                paymethod['actname'] = request.form['PaymentAccount']
                paymethod['currency'] = request.form['PaymentCurrency']
                paymethod['debit'] = request.form['debit']
                paymethod['credit'] = 0

                InvoicesAPI.EditBill(session['username'], session['password'], billcode,
                request.form['PaymentDate'], 'reception',
                request.form.getlist('account-type'),
                request.form.getlist('account-category'),
                request.form.getlist('account-name'),
                request.form.getlist('currency'),
                paymethod['credit'],
                request.form.getlist('credit'),
                request.form.getlist('description'),
                paymethod,
                request.form['comments']
                ) 
                flash('Bill successfully created...', category = 'success')
                return redirect(url_for('invoices.ReceptionBill'))
            except Exception as e:
                flash(str(e), category = 'fail')
                return redirect(url_for('invoices.ReceptionBill'))
    
    return render_template('invoices/edit_reception_bill.html', username = session['username'], 
    bills = bills,
    data1 = data1,
    data2 = data2)

@mod.route('view_reception_bill/<billcode>', methods = ['GET','POST'])
def ViewReceptionBill(billcode):
    Appr = InvoicesAPI.BillApproversList()
    bills = InvoicesAPI.GetBills('payment')
    paymethod = {}
    data1, data2 = InvoicesAPI.GetOneBill(billcode, 'reception')
    if request.method == 'POST':
        if request.form['submit'] == 'Submit'and session['username'] in Appr:
            try:
                InvoicesAPI.RegisterBill(session['username'], session['password'], billcode, request.form['status'])
                flash('Bill registered successfully...', category = 'success')
                return redirect(url_for('invoices.ReceptionBill'))
            except Exception as e:
                flash(str(e), category = 'fail')
                return redirect(url_for('invoices.ReceptionBill'))
        else:
            flash('This user does not have permission to register this bill...', category = 'fail')
            return redirect(url_for('invoices.ViewReceptionBill', billcode = billcode))
    return render_template('invoices/view_reception_bill.html', username = session['username'], 
    bills = bills,
    data1 = data1,
    data2 = data2)

# REST Routes
@mod.route('/Get-Accounts/<acc>')
def GetAccount(acc):
    Accounts = InvoicesAPI.GetAccount(acc)
    return jsonify(Accounts)

@mod.route('/Get-Pack/<code>')
def GetPack(code):
    Packs = InvoicesAPI.GetPack(code)
    return jsonify(Packs)
