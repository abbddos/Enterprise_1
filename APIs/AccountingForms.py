from flask_wtf import *
from wtforms import *
from wtforms.validators import *

class CategoryForm(Form):
    CategoryName = StringField('Category Name:', validators = [DataRequired()])
    CategoryDescription = TextAreaField('Description: ')

class Accounts(Form):
    AccountCode = StringField('Account Code:', validators = [DataRequired()])
    AccountName = StringField('Account Name:', validators = [DataRequired()])
    Currency = SelectField('Currency: ', choices = [], validators = [DataRequired()])
    OpeningBalance = StringField('Opening Balance:', validators = [DataRequired()])
    CurrentBalance = StringField('Current Balance:', validators = [DataRequired()])
    Comments = TextAreaField('Comments:')

class Currencies(Form):
    CurrencyName = StringField('Currency Name:', validators = [DataRequired()])
    CurrencyCode = StringField('Currency Code:', validators = [DataRequired()])
    ExchageRate = StringField('Exchange rate:', validators = [DataRequired()])
    Functional = SelectField('Functional Currency: ', choices = [
        ('Yes','Yes'),
        ('No','No')
    ])



