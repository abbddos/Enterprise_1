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

app = Flask(__name__)
sk = str(random.randint(1, 101))
app.secret_key = sk
app.config['DEBUG'] = True
app.config['TESTING'] = False
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'abbddos@gmail.com'
app.config['MAIL_PASSWORD'] = 'AbdulRahman*SS1983'
app.config['MAIL_DEFAULT_SENDER'] = 'abbddos@gmail.com'

csrf = CSRFProtect(app)
#csrf.init_app(app)
mail = Mail(app)

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
    return redirect(url_for('login'))

@app.route('/forgot_password', methods = ['GET','POST'])
def ForgotPassword():
    form = EnterForms.ForgotPassword(request.form)
    return render_template('forgot_password.html', form = form)

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
