from flask import *
from flask_mail import *
from APIs import EnterForms
from  APIs import EnterpriseAPI
import pdfkit
import datetime
import app

mod = Blueprint('logistics', __name__, url_prefix = '/logistics')

# ........ Logistics Group.
# ........ This group of applications addresses the basic working needs of...
# ........ logistics team in a company or institution. This group of urls ...
# ........ allows users to control, create and edit providers, items, ...
# ........ items gropus, packages, warehouses and their contents, ...
# ........ record all warehouse inbound and outbound transactions, ...
# ........ keeping inventory and producing required reports.
@mod.route('/')
def logistics():
    wh = EnterpriseAPI.GetWareHouses()
    return render_template('logistics/logistics.html', username = session['username'], wh = wh)

@mod.route('/Providers/', methods = ['GET' ,'POST'])
def Providers():
    form = EnterForms.ProvidersForm(request.form)
    data = EnterpriseAPI.GetProviders()
    wh = EnterpriseAPI.GetWareHouses()
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
                return redirect(url_for('logistics.Providers'))
            except Exception as e:
                flash(str(e), category = 'fail')
                return redirect(url_for('logistics.Providers'))
    return render_template('logistics/providers.html', username = session['username'], form = form, data = data, wh = wh)

@mod.route('/edit_provider/<prv>/', methods = ['GET', 'POST'])
def edit_provider(prv):
    wh = EnterpriseAPI.GetWareHouses()
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
                return redirect(url_for('logistics.Providers'))
            except Exception as e:
                flash(str(e), category = 'fail')
                return redirect(url_for('logistics.Providers'))
    return render_template('logistics/edit_provider.html', username = session['username'], form = form, data = data, data1 = data1, wh = wh)

@mod.route('/groups/', methods = ['GET','POST'])
def groups():
    data = EnterpriseAPI.GroupList()
    wh = EnterpriseAPI.GetWareHouses()
    if request.method == 'POST':
        if request.form['submit'] == 'Submit':
            try:
                EnterpriseAPI.AddGroup(session['username'], session['password'],
                request.form['Name'],
                request.form['description'])
                flash('Group added successfully', category = 'success')
                return redirect(url_for('logistics.groups'))
            except Exception as e:
                flash(str(e), category = 'fail')
                return redirect(url_for('logistics.groups'))
    return render_template('logistics/groups.html', username = session['username'], data = data, wh = wh)

@mod.route('/edit_group/<id>/', methods = ['GET','POST'])
def edit_group(id):
    data = EnterpriseAPI.GetGroup(id)
    data1 = EnterpriseAPI.GroupList()
    wh = EnterpriseAPI.GetWareHouses()
    if request.method == 'POST':
        if request.form['submit'] == 'Submit':
            try:
                EnterpriseAPI.UpdateGroup(session['username'], session['password'], id,
                request.form['Name'],
                request.form['description'])
                flash('Group Updated Successfully', category = 'success')
                return redirect(url_for('logistics.groups'))
            except Exception as e:
                flash(str(e), category = 'fail')
                return redirect(url_for('logistics.groups'))
    return render_template('logistics/edit_group.html', data = data, data1 = data1, username = session['username'], wh = wh)

@mod.route('/items/', methods = ['GET','POST'])
def items():
    form = EnterForms.ItemsForm(request.form)
    data = EnterpriseAPI.GetItems()
    wh = EnterpriseAPI.GetWareHouses()
    form.Group.choices = EnterpriseAPI.Groups()
    form.SecondaryUnit.choices = EnterpriseAPI.SecondaryUnits()
    form.Provider.choices = EnterpriseAPI.ProvidersList()
    if request.method == 'POST':
        if request.form['submit'] == 'Submit' and form.validate():
            #try:
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
            return redirect(url_for('logistics.items'))
            #except Exception as e:
            #    flash(str(e), category = 'fail')
            #    return redirect(url_for('logistics.items'))
    return render_template('logistics/items.html', username = session['username'], form = form, data = data, wh = wh)

@mod.route('/edit_item/<itm>/', methods = ['GET','POST'])
def edit_item(itm):
    data = EnterpriseAPI.GetItems()
    data1 = EnterpriseAPI.FetchItem(itm)
    provs = EnterpriseAPI.ProvidersList()
    grp = EnterpriseAPI.Groups()
    secunit = EnterpriseAPI.SecondaryUnits()
    wh = EnterpriseAPI.GetWareHouses()
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
                return redirect(url_for('logistics.items'))
            except Exception as e:
                flash(str(e), category = 'fail')
                return redirect(url_for('logistics.items'))
    return render_template('logistics/edit_item.html', username = session['username'], data = data, data1 = data1, provs = provs, grp = grp, wh = wh, secunit = secunit)

@mod.route('/packages/', methods = ['GET','POST'])
def packages():
    itms = EnterpriseAPI.ItemPicker()
    pkg = EnterpriseAPI.GetPackages()
    wh = EnterpriseAPI.GetWareHouses()
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
                return redirect(url_for('logistics.packages'))
            except Exception as e:
                i = str(request.form.getlist('unit'))
                flash(str(e), category = 'fail')
                return redirect(url_for('logistics.packages'))

    return render_template('logistics/packages.html', username = session['username'], itms = itms, pkg = pkg, wh = wh)

@mod.route('/edit_package/<pkg>/', methods = ['GET','POST'])
def edit_package(pkg):
    pks, itms = EnterpriseAPI.FetchPackage(pkg)
    pkk = EnterpriseAPI.GetPackages()
    itt = EnterpriseAPI.ItemPicker()
    wh = EnterpriseAPI.GetWareHouses()
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
                return redirect(url_for('logistics.packages'))
            except Exception as e:
                flash(str(e), category = 'fail')
                return redirect(url_for('logistics.packages'))
    return render_template('logistics/edit_package.html', username = session['username'], pks = pks, itms = itms, pkk = pkk, itt = itt, wh = wh)

@mod.route('Secondary_units/', methods = ['GET','POST'])
def SecondaryUnits():
    data = EnterpriseAPI.GetSecondaryUnits()
    wh = EnterpriseAPI.GetWareHouses()
    if request.method == 'POST':
        if request.form['submit'] == 'Submit':
            try:
                EnterpriseAPI.CreateSecondaryUnit(session['username'], session['password'],
                request.form['secuntname'],
                request.form['secuntcode'],
                request.form['unit'],
                request.form['secuntmeasure'])
                flash('Secondary unit created successfully...', category = 'success')
                return redirect(url_for('logistics.SecondaryUnits'))
            except Exception as e:
                flash(str(e), category = 'fail')
                return redirect(url_for('logistics.SecondaryUnits'))
    return render_template('logistics/Secondary_units.html', username = session['username'], data = data, wh = wh)

@mod.route('Edit_Secondary_unit/<code>/', methods = ['GET','POST'])
def EditSecondaryUnit(code):
    data = EnterpriseAPI.GetSecondaryUnits()
    data1 = EnterpriseAPI.GrabSecondaryUnit(code)
    wh = EnterpriseAPI.GetWareHouses()
    if request.method == 'POST':
        if request.form['submit'] == 'Submit':
            try:
                EnterpriseAPI.UpdateSecondaryUnit(session['username'], session['password'],
                request.form['secuntname'],
                code,
                request.form['unit'],
                request.form['secuntmeasure'])
                flash('Secondary Unit updated successfully...', category = 'success')
                return redirect(url_for('logistics.SecondaryUnits'))
            except Exception as e:
                flash(str(e), category = 'fail')
                return redirect(url_for('logistics.SecondaryUnits'))
    return render_template('logistics/Edit_secondary_unit.html', username = session['username'], data = data, data1 = data1, wh = wh)

@mod.route('/warehouses/create_warehouse/', methods = ['GET','POST'])
def create_warehouse():
    form = EnterForms.WarehouseForm(request.form)
    wh = EnterpriseAPI.GetWareHouses()
    if request.method == 'POST':
        if request.form['submit'] == 'Submit':
            try:
                EnterpriseAPI.CreateWarehouse(session['username'], session['password'],
                request.form['Name'],
                request.form['Code'],
                request.form['Location'],
                request.form['Description'])
                flash('Warehouse Created Successfully', category = 'success')
                return redirect(url_for('logistics.create_warehouse'))
            except Exception as e:
                flash(str(e), category = 'fail')
                return redirect(url_for('logistics.create_warehouse'))
    return render_template('logistics/create_warehouse.html', form = form, wh = wh, username = session['username'])

@mod.route('/warehouses/edit_warehouse/<code>/', methods = ['GET','POST'])
def edit_warehouse(code):
    form = EnterForms.BinsForm(request.form)
    whh = EnterpriseAPI.FetchWarehouse(code)
    wh = EnterpriseAPI.GetWareHouses()
    bins = EnterpriseAPI.GetBins(code)
    if request.method == 'POST':
        if request.form['submit'] == 'Submit':
            try:
                EnterpriseAPI.UpdateWarehouse(session['username'], session['password'], code,
                request.form['Name'],
                request.form['Location'],
                request.form['Description'])
                flash('Warehouse Updated Successfully', category = 'success')
                return redirect(url_for('logistics.create_warehouse'))
            except Exception as e:
                flash(str(e), category = 'fail')
                return redirect(url_for('logistics.create_warehouse'))
    return render_template('logistics/edit_warehouse.html', whh = whh, wh = wh, bins = bins, username = session['username'], form = form, code = code)

@mod.route('/warehouses/edit_warehouse/add_bin/<wh>/', methods = ['GET','POST'])
def add_bin(wh):
    if request.method == 'POST':
        if request.form['submit'] == 'Submit':
            try:
                EnterpriseAPI.CreateBin(session['username'], session['password'],
                request.form['name'],
                request.form['code'],
                wh,
                request.form['status'],
                request.form['description'])
                flash('Bin successfully added', category = 'success')
                return redirect(url_for('logistics.edit_warehouse', code = wh))
            except Exception as e:
                flash(str(e), category = 'fail')
                return redirect(url_for('logistics.edit_warehouse', code = wh))
    return redirect(url_for('logistis/edit_warehouse', code = wh))

@mod.route('/warehouses/edit_warehouse/edit_bin/<whcode>/', methods = ['GET','POST'])
def edit_bin(whcode):
    if request.method == 'POST':
        if request.form['submit'] == 'Submit':
            try:
                EnterpriseAPI.UpdateBin(session['username'], session['password'],
                request.form['Bcode'],
                request.form['Bname'],
                request.form['Bstatus'],
                request.form['Bdesc'])
                flash('Bin updated successfully', category = 'success')
                return redirect(url_for('logistics.edit_warehouse', code = whcode))
            except Exception as e:
                flash(str(e), category = 'fail')
                return redirect(url_for('logistics.edit_warehouse', code = whcode))
    return redirect(url_for('logistis/edit_warehouse', code = whcode))

@mod.route('/transactions', methods = ['GET','POST'])
def transactions():
    itms = EnterpriseAPI.ItemPicker()
    pkgs = EnterpriseAPI.PackagePicker()
    wh = EnterpriseAPI.GetWareHouses()
    warehouse = EnterpriseAPI.GetWareHouses()
    trans = EnterpriseAPI.GetTrans()
    rqst = EnterpriseAPI.ApprRequests()
    if request.method == 'POST':
        if request.form['submit'] == 'Submit':
            try:
                if request.form['transaction-type'] == 'Inbound':
                    transid = EnterpriseAPI.InboundTransaction(session['username'],session['password'],
                    request.form.getlist('Name'),
                    request.form.getlist('code'),
                    request.form['warehouse'],
                    request.form.getlist('bins'),
                    request.form.getlist('unit'),
                    request.form.getlist('quantity'),
                    request.form['transaction-status'],
                    request.form['comments'])
                    flash('Inbound transaction recorded...', category = 'success')
                    return redirect(url_for('logistics.transactions'))

                elif request.form['transaction-type'] == 'Outbound':
                    transid = EnterpriseAPI.OutboundTransaction(session['username'],session['password'],
                    request.form.getlist('Name'),
                    request.form.getlist('code'),
                    request.form['warehouse'],
                    request.form.getlist('bins'),
                    request.form.getlist('unit'),
                    request.form.getlist('quantity'),
                    request.form['transaction-status'],
                    request.form['comments']) 
                    flash('Outbound transaction recorded...', category = 'success')
                    return redirect(url_for('logistics.transactions'))
            except Exception as e:
                flash(str(e), category = 'fail')
                return redirect(url_for('logistics.transactions'))
    return render_template('logistics/transactions.html', username = session['username'], itms = itms, pkgs = pkgs, warehouse = warehouse, wh = wh, trans = trans, rqst = rqst)

@mod.route('/edit_transaction/<transid>', methods = ['GET','POST'])
def edit_transaction(transid):
    wh = EnterpriseAPI.GetWareHouses()
    warehouse = EnterpriseAPI.GetWareHouses()
    trans = EnterpriseAPI.GetTrans()
    head, details = EnterpriseAPI.TransInfo(transid)
    rqst = EnterpriseAPI.ApprRequests()
    if request.method == 'POST':
        if request.form['submit'] == 'Submit':
            try:
                EnterpriseAPI.UpdateTransaction(session['username'], session['password'], transid, request.form['transaction-status'], request.form['comments'])
                flash('Transaction updated...', category = 'success')
                return redirect(url_for('logistics.transactions'))
            except Exception as e:
                flash('Cannot to update a Complete or Canceled transacction.', category = 'fail')
                return redirect(url_for('logistics.edit_transaction', transid = transid))
    return render_template('logistics/edit-transaction.html', username = session['username'], warehouse = warehouse, wh = wh, trans = trans, head = head, details = details, rqst = rqst)

@mod.route('/requests', methods = ['GET','POST'])
def requests():
    trans = EnterpriseAPI.GetRequests()
    itms = EnterpriseAPI.ItemPicker()
    pkgs = EnterpriseAPI.PackagePicker()
    wh = EnterpriseAPI.GetWareHouses()
    appr = EnterpriseAPI.InvApprovers()
    if request.method == 'POST':
        if request.form['submit'] == 'Submit':
            if (request.form['status'] == 'Approved' or request.form['status'] == 'Rejected') and request.form['approver'] != session['username']:
                flash("Can't proceed with request, approver's permission is required.", category = 'fail')
                return redirect(url_for('logistics.requests'))
            else:
                try:
                    data, code = EnterpriseAPI.CreateRequest(session['username'], session['password'],
                    request.form['type'],
                    request.form['status'],
                    request.form['approver'],
                    request.form['comments'],
                    request.form.getlist('code'),
                    request.form.getlist('Name'),
                    request.form.getlist('unit'),
                    request.form.getlist('quantity'))

                    msg = Message('New Inventory request', recipients = [data[2]])
                    msg.body = "Dear {}, \n Please note that new inventory request, code: {} has been created and requires your approval or rejection.".format(data[0], code) 
                    app.mail.send(msg)

                    flash('Request successfully added.', category = 'success')
                    return redirect(url_for('logistics.requests'))
                except Exception as e:
                    flash(str(e), category = 'fail')
                    return redirect(url_for('logistics.requests'))
    return render_template('logistics/requests.html', username = session['username'], trans = trans, wh = wh, itms = itms, pkgs = pkgs, appr = appr)

@mod.route('edit_request/<reqid>', methods = ['GET','POST'])
def edit_request(reqid):
    trans = EnterpriseAPI.GetRequests()
    itms = EnterpriseAPI.ItemPicker()
    pkgs = EnterpriseAPI.PackagePicker()
    wh = EnterpriseAPI.GetWareHouses()
    appr = EnterpriseAPI.InvApprovers()
    head, details, aprv = EnterpriseAPI.ReqInfo(reqid)
    if request.method == 'POST':
        if request.form['submit'] == 'Submit':
            if (request.form['status'] == 'Approved' or request.form['status'] == 'Rejected') and request.form['approver'] != session['username']:
                flash("Can't proceed with request, approver's permission is required.", category = 'fail')
                return redirect(url_for('logistics.requests'))
            else: 
                try:
                    EnterpriseAPI.UpdateRequest(session['username'], session['password'], request.form['status'], request.form['comments'], reqid)
                    flash('Request Updated', category = 'success')
                    return redirect(url_for('logistics.requests'))
                except Exception as e:
                    flash(str(e), category = 'fail')
                    return redirect(url_for('logistics.requests'))
    return render_template('logistics/edit_request.html', username = session['username'], trans = trans, wh = wh, appr = appr, head = head, details = details, aprv = aprv)

@mod.route('/warehouse_inventory', methods = ['GET','POST'])
def warehouse_inventory():
    wh = EnterpriseAPI.GetWareHouses()
    if request.method =='POST':
        if request.form['submit'] == 'Submit':
            if request.form['to-date'] < request.form['from-date']:
                flash('Error: To date must be later than from date', category = 'fail')
                return redirect(url_for('logistics.warehouse_inventory'))
            else:
                if request.form['file-type'] == 'csv':
                    file = EnterpriseAPI.Warehouse_Inventory_to_CSV(session['username'], session['password'], 
                    request.form['from-date'],
                    request.form['to-date'],
                    request.form.getlist('wh_check'))
                    response = make_response(file)
                    response.headers['Content-type'] = 'text/csv'
                    response.headers['Content-Disposition'] = 'attachement; filename = warehouse_inventory_report.csv'
                    return response
                elif request.form['file-type'] == 'pdf':
                    data = EnterpriseAPI.Warehouse_Inventory_to_PDF(session['username'], session['password'], 
                    request.form['from-date'],
                    request.form['to-date'],
                    request.form.getlist('wh_check'))
                    reportdate = datetime.datetime.now()
                    rendered = render_template('/logistics/warehouse_inventory.html', reportdate = reportdate, whs = request.form.getlist('wh_check'), data = data )
                    pdf = pdfkit.from_string(rendered, False)
                    response = make_response(pdf)
                    response.headers['Content-type'] = 'application/pdf'
                    response.headers['Content-Disposition'] = 'attachement; filename = warehouse-inventory-report.pdf'
                    return response
    return render_template('logistics/warehouse-inventory-report.html', username = session['username'], wh = wh)

@mod.route('/items_packages_inventory', methods = ['GET','POST'])
def items_packages_inventory():
    wh = EnterpriseAPI.GetWareHouses()
    itms = EnterpriseAPI.ItemPicker()
    pkgs = EnterpriseAPI.PackagePicker()
    if request.method == 'POST':
        if request.form['submit'] == 'Submit':
            if request.form['to-date'] < request.form['from-date']:
                flash('Error: To date must be later than from date', category = 'fail')
                return redirect(url_for('logistics.warehouse_inventory'))
            else:
                if request.form['file-type'] == 'csv':
                    file = EnterpriseAPI.Items_Packs_Inventory_to_CSV(session['username'], session['password'],
                    request.form['from-date'],
                    request.form['to-date'],
                    request.form.getlist('itm_check'),
                    request.form.getlist('pkg_check'))
                    response = make_response(file)
                    response.headers['Content-type'] = 'text/csv'
                    response.headers['Content-Disposition'] = 'attachement; filename = items-packs_inventory_report.csv'
                    return response
                elif request.form['file-type'] == 'pdf':
                    data = EnterpriseAPI.Items_Packs_Inventory_to_PDF(session['username'], session['password'],
                    request.form['from-date'],
                    request.form['to-date'],
                    request.form.getlist('itm_check'),
                    request.form.getlist('pkg_check'))
                    reportdate = datetime.datetime.now()
                    rendered = render_template('/logistics/item-pack-inventory-report.html', reportdate = reportdate, itm = request.form.getlist('itm_check'), pkg = request.form.getlist('pkg_check'), data = data )
                    pdf = pdfkit.from_string(rendered, False)
                    response = make_response(pdf)
                    response.headers['Content-type'] = 'application/pdf'
                    response.headers['Content-Disposition'] = 'attachement; filename = item-pack-inventory-report.pdf'
                    return response
    return render_template('logistics/item-package-inventory-report.html', username = session['username'], wh = wh, itms = itms, pkgs = pkgs)

@mod.route('/bins_report', methods = ['GET','POST'])
def bins_report():
    wh = EnterpriseAPI.GetWareHouses()
    if request.method == 'POST':
        if request.form['submit'] == 'Submit':
            if request.form['file-type'] == 'csv':
                file = EnterpriseAPI.Bins_Report_to_CSV(session['username'], session['password'], request.form.getlist('wh_check'))
                response = make_response(file)
                response.headers['Content-type'] = 'text/csv'
                response.headers['Content-Disposition'] = 'attachement; filename = items-packs_inventory_report.csv'    
                return response
            elif request.form['file-type'] == 'pdf':
                data = EnterpriseAPI.Bins_Report_to_PDF(session['username'], session['password'], request.form.getlist('wh_check'))
                reportdate = datetime.datetime.now()
                rendered = render_template('logistics/bins_report.html', data = data, reportdate = reportdate)
                pdf = pdfkit.from_string(rendered, False)
                response = make_response(pdf)
                response.headers['Content-type'] = 'application/pdf'
                response.headers['Content-Disposition'] = 'attachement; filename = bins-statuses-report.pdf'
                return response
    return render_template('logistics/bins-report.html', username = session['username'], wh = wh)

@mod.route('/transactions_report', methods = ['GET','POST'])
def transactions_report():
    wh = EnterpriseAPI.GetWareHouses()
    if request.method == 'POST':
        if request.form['submit'] == 'Submit':
            if request.form['file-type'] == 'csv':
                file = EnterpriseAPI.Transactions_Report_to_CSV(session['username'], session['password'])
                response = make_response(file)
                response.headers['Content-type'] = 'text/csv'
                response.headers['Content-Disposition'] = 'attachement; filename = items-packs_inventory_report.csv'
                return response
            elif request.form['file-type'] == 'pdf':
                data1 = EnterpriseAPI.Transactions_Report_to_PDF(session['username'], session['password'])
                reportdate = datetime.datetime.now()
                rendered = render_template('logistics/transactions_report.html', reportdate = reportdate, data1 = data1)
                pdf = pdfkit.from_string(rendered, False)
                response = make_response(pdf)
                response.headers['Content-type'] = 'application/pdf'
                response.headers['Content-Disposition'] = 'attachement; filename = transactions-report.pdf'
                return response
    return render_template('logistics/transactions-report.html', username = session['username'], wh = wh)

@mod.route('/print_invoice/<transid>/<transby>/<transtype>/<transtatus>/<wh>')
def print_invoice(transid, transby, transtype, transtatus, wh):
    data, cmnt = EnterpriseAPI.TransInvoice(transid)
    transdate = str(datetime.datetime.now())
    rendered = render_template('logistics/transaction-invoice.html', transid = transid, transdate = cmnt[0], transtype = transtype, transby = transby, transtatus = transtatus, wh = wh, data = data, cmnt = cmnt)
    pdf = pdfkit.from_string(rendered, False)
    response = make_response(pdf)
    response.headers['Content-type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachement; filename = transaction-invoice.pdf'
    return response