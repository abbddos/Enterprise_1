from flask import *
from flask_mail import *
from flask_wtf.csrf import CSRFProtect, CSRFError
import random
from APIs import EnterForms
from APIs.EnterpriseAPI import *
from views import profile
from views import users
from views import logistics
from views import accounting
from views import invoices
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import EnterpriseConfig

app = Flask(__name__)
sk = str(random.randint(1, 101))
app.secret_key = sk
app.config['DEBUG'] = True
app.config['TESTING'] = False
app.config['MAIL_SERVER'] = EnterpriseConfig.Mail_Server
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = EnterpriseConfig.Email_Username
app.config['MAIL_PASSWORD'] = EnterpriseConfig.Email_Password
app.config['MAIL_DEFAULT_SENDER'] = EnterpriseConfig.Email_Username

csrf = CSRFProtect(app)
#csrf.init_app(app)
mail = Mail(app)


def ForgotPasswordToken(email):
    con, cur = root()
    try:
        cur.execute("SELECT firstname, username FROM users WHERE email = %s ", (email,))
        usr = cur.fetchone()
        con.close()

        s = Serializer(app.secret_key, 1800)
        token = s.dumps({'user':usr[1]}).decode('utf-8')
        return usr, token
    except:
        con.close()
        return None, None

def VerifyToken(token):
    s = Serializer(app.secret_key)
    try:
        usr = s.loads(token)['user']
    except:
        return None
    return usr

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = EnterForms.LoginForm(request.form)
    if request.method == 'POST':
        if request.form['submit'] == 'Login' and form.validate():
            username = request.form['usrname']
            passwd = request.form['passwd']
            logger = Logger(username, passwd)
            if logger['logged'] == True:
                session['username'] = logger['username']
                session['password'] = logger['password']
                session['role'] = logger['role']
                return redirect(url_for('home'))
            elif logger['logged'] == False:
                flash('LOGIN ERROR: Bad username or password', category = 'fail')
                return render_template('login.html', form = form)

    return render_template('login.html', form = form)

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('password', None)
    session.pop('role', None)
    return redirect(url_for('login'))

@app.route('/forgot_password', methods = ['GET','POST'])
def ForgotPassword():
    form = EnterForms.ForgotPassword(request.form)
    if request.method == 'POST':
        if request.form['submit'] == 'Submit':
            try:
                usr, token = ForgotPasswordToken(request.form['email'])
                if token is not None:
                    msg = Message('New Enterprise Account', recipients = [str(request.form['email'])])
                    msg.body = "Dear {}:\n please follow the link below to change your password. \n Thank you for using Enterprise. \n {}".format(usr[0], url_for('ChangeForgotPassword', usr = usr[1], token = token, _external=True))
                    mail.send(msg)
                    flash('An email was sent to your email account', category = 'success')
                    return redirect(url_for('ForgotPassword'))
                else:
                    flash('Email not found', category = 'fail')
                    return redirect(url_for('ForgotPassword'))
            except Exception as e:
                flash(str(e), category = 'fail')
                return redirect(url_for('ForgotPassword'))
    return render_template('forgot_password.html', form = form)

@app.route('/change_forgot_password/<token>', methods = ['GET','POST'])
def ChangeForgotPassword(token):
    form = EnterForms.ChangePassword(request.form)
    usr = VerifyToken(token)
    if usr:
        if request.method == 'POST':
            if request.form['submit'] == 'Submit' and request.form['newpswd'] == request.form['confirm']:
                try:
                    ChangePassword1(usr, request.form['newpswd'])
                    flash('Password changed...', category = 'success')
                    return redirect(url_for('login'))
                except Exception as e:
                    flash(str(e), category = 'fail')
                    return redirect(url_for('login'))
        return render_template('change_forgot_password.html', form = form, token = token)
    else:
        return render_template('invalid_token.html')

@app.route('/home')
def home():
    return render_template('home.html', username = session['username'], role = session['role'] )



# ........ JSON returning urls.
@app.route('/GrabItems')
def GrabItems():
    code = request.args['ItCode']
    try:
        item = ItemAdder(code)
        for i in item:
            return jsonify(msg = 'success', itemcode = i[0], itemname = i[1], itemunit = i[2], unitprice = i[3], unitcost = i[4])
    except Exception as e:
        return jsonify(msg = str(e))

@app.route('/GrabPacks')
def GrabPacks():
    code = request.args['PKCode']
    try:
        Pack = PackageAdder(code)
        for i in Pack:
            return jsonify(msg = 'success', packcode = i[0], packname = i[1])
    except Exception as e:
        return jsonify(msg = str(e))

@app.route('/GrabBin')
def GrabBin():
    code = request.args['BCode']
    try:
        bn = BinInfo(code)
        return jsonify(msg = 'success', BinCode = bn[0], BinName = bn[1], BinStatus = bn[3], BinDesc = bn[2])
    except Exception as e:
        return jsonify(msg = str(2))

@app.route('/GetBin/<code>')
def GetBin(code):
    BIN = GrabBins(code)
    BINS = []
    for s in BIN:
        BINS.append(s[0])
    return jsonify(bins = BINS)

#@app.route('/testing', methods = ['GET','POST'])
#def testing():

#    if request.method == 'POST':
#        field = request.form.getlist('fuckit')
#        return str(field)
#    return render_template('tester.html')

app.register_blueprint(profile.mod)
app.register_blueprint(users.mod)
app.register_blueprint(logistics.mod)
app.register_blueprint(accounting.mod)
app.register_blueprint(invoices.mod)

#if __name__ == '__main__':
#    app.run(debug = True)
