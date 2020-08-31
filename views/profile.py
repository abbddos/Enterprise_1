from flask import *
#from flask_mail import *
from APIs import EnterForms
from  APIs import EnterpriseAPI

# ........This url is linked to UpdateProfile API at Model.py to allow...
# ........user to view, edit and update his/her profile information...
# ........including and limited to First Name, Last Name, Coontact...
# ....... information and position without changing password or username.

mod = Blueprint('profile', __name__, url_prefix = '/profile')

@mod.route('/view_profile/user_profile/<user>/', methods = ['GET', 'POST'])
def user_profile(user):
    if user == 'admin':
        return redirect(url_for('profile.change_password', user = user))
    else:
        data = EnterpriseAPI.GetUser(user)
        if request.method == 'POST':
            if request.form['submit'] == 'Submit':
                try:
                    EnterpriseAPI.UpdateProfile(request.form['firstname'],
                    request.form['lastname'],
                    request.form['email'],
                    request.form['phone1'],
                    request.form['phone2'], user)
                    flash('Profile Updated Successfully', category = 'success')
                    return redirect(url_for('profile.user_profile', user = user))
                except Exception as e:
                    flash(str(e), category = 'fail')
        return render_template('profile/user_profile.html', user = user, username = session['username'], role = session['role'], data = data)

# ........ This url is lined to ChangePassword API at Model.py to allow...
# ........ user to change his/her password.
@mod.route('/view_profile/change_password/<user>/', methods = ['GET' ,'POST'])
def change_password(user):
    form = EnterForms.ChangePassword(request.form)
    if request.method == 'POST':
        if request.form['submit'] == 'Submit' and form.validate():
            try:
                EnterpriseAPI.ChangePassword(user, request.form['currentpswd'], request.form['newpswd'])
                flash('Password changed successfully', category = 'success')
                return redirect(url_for('profile.change_password', user = user))
            except Exception as e:
                flash(str(e), category = 'fail')
        else:
            flash('Passwords must match', category = 'fail')
            return render_template('profile/change_password.html', username = session['username'], role = session['role'], user = user, form = form)
    return render_template('profile/change_password.html', username = session['username'], role = session['role'], user = user, form = form)
