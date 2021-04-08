from flask import *
from flask_mail import *
import app
from APIs import EnterForms
from  APIs import EnterpriseAPI
import os
from APIs import AccountingForms
from  APIs import AccountingAPI


mod = Blueprint('users', __name__, url_prefix = '/users')

@mod.route('/')
def admin():
    return render_template('users/admin.html', username = session['username'])

# ........ Creating new user indivisually using the CreateUser...
# ........ API at Model.py.
@mod.route('/create_user/', methods = ['GET', 'POST'])
def create_user():
    form = EnterForms.CreateUser(request.form)
    data = EnterpriseAPI.GetUsers()
    if request.method == 'POST':
        if request.form['submit'] == 'Submit' and form.validate():
            try:
                usrname, pswd = EnterpriseAPI.CreateUser(session['username'], session['password'],
                request.form['firstname'],
                request.form['lastname'],
                request.form['company'],
                request.form['position'],
                request.form['department'],
                request.form['email'],
                request.form['phone1'],
                request.form['phone2'],
                request.form.getlist('role-check'),
                request.form.getlist('appr-check'))
                msg = Message('New Enterprise Account', recipients = [str(request.form['email'])])
                msg.body = "Dear {}, \n Thank you for using Enterprise. please note that your username is: {} and your password is {}. \n It is highly recommended that you change your password as soon as possible. \n Thank you for using Enterprise.".format(str(request.form['firstname']), str(usrname), str(pswd)) 
                app.mail.send(msg)
                flash('User Created Successfully', category = 'success')
                return redirect(url_for('users.create_user'))
            except Exception as e:
                flash(str(e), category = 'fail')
                return render_template('users/create_user.html', username = session['username'], role = session['role'], data = data, form = form)
    return render_template('users/create_user.html', username = session['username'], role = session['role'], data = data, form = form )

# ........ Resetting user password to initial default password.
@mod.route('/reset_password/<user>/')
def reset_password(user):
    try:
        NewPass, Name = EnterpriseAPI.ResetPassword(session['username'], session['password'], user)
        flash('User Password was reset', category = 'success')
        msg = Message('Enterprise password reset', recipients = [str(Name[2])])
        msg.body = "Dear {}, \n Please note that your password has been reset into {} . \n Please note it is highly adviised that you change your password soon. \n Thank you for using Enterprise.".format(Name[0], NewPass)
        app.mail.send(msg)
        return redirect(url_for('users.create_user'))
    except Exception as e:
        flash(str(e), category = 'fail')
        return redirect(url_for('users.create_user'))




# ........ Updating user information using UpdateUser API at Model.py
# ........ This allows administrators to update users' info and assigned...
# ........ privilages.
@mod.route('/edit_user/<id>/', methods = ['GET', 'POST'])
def edit_user(id):
    data1 = EnterpriseAPI.GetUsers()
    data2 = EnterpriseAPI.GetUserInfo(id)
    data3 = EnterpriseAPI.GetApprovals(data2[0][3])
    if request.method == 'POST':
        if request.form['submit'] == 'Submit':
            try:
                EnterpriseAPI.UpdateUser(session['username'], session['password'], id,
                request.form['firstname'],
                request.form['lastname'],
                request.form['company'],
                request.form['position'],
                request.form['department'],
                request.form['email'],
                request.form['phone1'],
                request.form['phone2'],
                request.form.getlist('role-check'),
                request.form['status'],
                request.form.getlist('appr-check'), data2[0][3])
                flash('User Updated Successfully', category = 'success')
                return redirect(url_for('users.create_user'))
            except Exception as e:
                flash(str(e), category = 'fail')
                return redirect(url_for('users.create_user'))
    return render_template('users/edit_user.html', username = session['username'], role = session['role'], data1 = data1, data2 = data2, data3 = data3 )

@mod.route('/Company-Profile', methods = ['GET','POST'])
def CompanyProfile():
    profile = EnterpriseAPI.GetCompanyProfile()
    if request.method == 'POST':
        if request.form['submit'] == 'Submit':
            try:
                EnterpriseAPI.UpdateCompanyProfile(session['username'], session['password'],
                request.form['companyname'],
                request.form['companyaddress'],
                request.form['phone1'],
                request.form['phone2'],
                request.form['email'],
                request.form['pobox'],
                request.form['registration'],
                request.form['description'])
                flash('Company profile updated succcessfully', category = 'success')
                return redirect(url_for('users.CompanyProfile'))
            except Exception as e:
                flash(str(e), category = 'fail')
                return redirect(url_for('users.CompanyProfile'))
    return render_template('users/company_profile.html', username = session['username'], role = session['role'], pro = profile)

@mod.route('/currencies_settings', methods = ['GET','POST'])
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
                    return redirect(url_for('users.currencies'))
                else:
                    flash('You already have a functional currency', category = 'fail')
                    return redirect(url_for('users.currencies'))
            except Exception as e:
                flash(str(e), category = 'fail')
                return redirect(url_for('users.currencies'))
    return render_template('users/currencies.html', username = session['username'], role = session['role'], form = form, data = data, data1 = data1)

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
                    return redirect(url_for('users.currencies'))
                else:
                    flash('You already have a functional currency', category = 'fail')
                    return redirect(url_for('users.EditCurrency', code = code))
            except Exception as e:
                flash(str(e), category = 'fail')
                return redirect(url_for('users.currencies'))
    return render_template('users/edit_currency.html', username = session['username'], role = session['role'], data = data, data1 = data1, data2 = data2)

@mod.route('/change_admin_password/<user>/', methods = ['GET' ,'POST'])
def change_admin_password(user):
    form = EnterForms.ChangePassword(request.form)
    if request.method == 'POST':
        if request.form['submit'] == 'Submit' and form.validate():
            try:
                EnterpriseAPI.ChangePassword(user, request.form['currentpswd'], request.form['newpswd'])
                flash('Password changed successfully', category = 'success')
                return redirect(url_for('users.change_admin_password', user = user))
            except Exception as e:
                flash(str(e), category = 'fail')
        else:
            flash('Passwords must match', category = 'fail')
            return render_template('users/change_password.html', username = session['username'], role = session['role'], user = user, form = form)
    return render_template('users/change_password.html', username = session['username'], role = session['role'], user = user, form = form)
