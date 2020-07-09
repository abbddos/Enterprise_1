from flask_wtf import *
from wtforms import *
from wtforms.validators import *

class LoginForm(Form):
    usrname = StringField('Username: ', validators = [DataRequired()])
    passwd = PasswordField('Password: ', validators = [DataRequired()])

class ChangePassword(Form):
    currentpswd = PasswordField('Current Password: ', validators = [DataRequired()])
    newpswd = PasswordField('New Password: ', validators = [DataRequired(), EqualTo('confirm', message = 'Passwords must match')])
    confirm = PasswordField('Confirm New Password: ', validators = [DataRequired()])

class CreateUser(Form):
    firstname = StringField('First Name: ', validators = [DataRequired()])
    lastname = StringField('Last Name: ', validators = [DataRequired()])
    company = StringField('Company: ')
    position = StringField('Position: ')
    department = StringField('Department: ')
    email = StringField('Email: ')
    phone1 = StringField('Phone #1: ')
    phone2 = StringField('Phone #2: ')
    usrtype = SelectField('User Type: ', choices = [
    ('Admin', 'Admin'),
    ('User', 'User'),
    ('Viewer', 'Viewer')
    ])

class FileForm(Form):
    FileName = FileField('Select File: ', validators = [DataRequired()])

class ProvidersForm(Form):
    name = StringField('Name: ', validators = [DataRequired()])
    address = StringField('Address: ')
    phone1 = StringField('Phone #1: ')
    phone2 = StringField('Phone #2: ')
    email = StringField('Email: ')
    pobox = StringField('PO-BOX: ')
    description = TextAreaField('Description: ')

class ItemsForm(Form):
    #General
    ItemName = StringField('Item Name: ', validators = [DataRequired()])
    Brand = StringField('Brand: ', validators = [DataRequired()])
    Provider = SelectField('Provider', choices = [])
    Unit = SelectField('Unit', choices = [
    ('mm','mm'),
    ('cm','cm'),
    ('inch','inch'),
    ('foot','foot'),
    ('yard','yard'),
    ('meter','meter'),
    ('Km','Km'),
    ('mile','mile'),
    ('Gram','Gram'),
    ('Ounce','Ounce'),
    ('Lbs','Lbs'),
    ('Kg','Kg'),
    ('Ton','Ton'),
    ('cc','cc'),
    ('Liter','Liter'),
    ('US-Gal','US-Gal'),
    ('UK-Gal','UK-Gal'),
    ('Tank(20l)','Tank(20l)'),
    ('Piece','Piece')
    ], validators = [DataRequired()])
    UnitPrice = StringField('Unit Price: ', validators = [DataRequired()])
    UnitCost = StringField('Unit Cost:', validators = [DataRequired()])
    Group = SelectField('Group: ', choices = [])
    Category = SelectField('Category: ', choices = [
    ('Asset','Asset'),
    ('Non-Asset','Non-Asset')])
    SecondaryUnit = SelectField('Secondary Unit', choices = [])
    Description = TextAreaField('Description: ')

    #Size and dimentions
    Length = StringField('Length: ')
    LengthUnit = SelectField('Length Unit: ', choices = [
    ('mm','mm'),
    ('cm','cm'),
    ('inch','inch'),
    ('foot','foot'),
    ('yard','yard'),
    ('meter','meter'),
    ('Km','Km'),
    ('mile','mile')])
    Width = StringField('Width: ')
    WidthUnit = SelectField('Width Unit: ', choices = [
    ('mm','mm'),
    ('cm','cm'),
    ('inch','inch'),
    ('foot','foot'),
    ('yard','yard'),
    ('meter','meter'),
    ('Km','Km'),
    ('mile','mile')])
    Height = StringField('Height / Thickness: ')
    HeightUnit = SelectField('Height/Thickness Unit: ', choices = [
    ('mm','mm'),
    ('cm','cm'),
    ('inch','inch'),
    ('foot','foot'),
    ('yard','yard'),
    ('meter','meter'),
    ('Km','Km'),
    ('mile','mile')])
    Diameter = StringField('Diameter: ')
    DiamaterUnit = SelectField('Diameter Unit: ', choices = [
    ('mm','mm'),
    ('cm','cm'),
    ('inch','inch'),
    ('foot','foot'),
    ('yard','yard'),
    ('meter','meter'),
    ('Km','Km'),
    ('mile','mile')])
    Size = StringField('Size(Category): ')
    #Specs and Numbers
    SKU = StringField('SKU: ')
    PartNumber = StringField('Part Number: ')
    IEME = StringField('IEME: ')
    #Color
    Color = StringField('Color: ')

class WarehouseForm(Form):
    Name = StringField('Name: ')
    Code = StringField('Code: ', validators = [DataRequired()])
    Location = StringField('Location: ')
    Description = TextAreaField('Description')

class BinsForm(Form):
    code = StringField('Code: ', validators = [DataRequired()])
    name = StringField('Name: ')
    status = SelectField('Status: ', choices = [('Open','Open'),('Locked','Locked')])
    description = TextAreaField('Description: ')

class CustomersForm(Form):
    name = StringField('Name: ', validators = [DataRequired()])
    address = StringField('Address: ')
    phone1 = StringField('Phone #1: ')
    phone2 = StringField('Phone #2: ')
    email = StringField('Email: ')
    pobox = StringField('PO-BOX: ')
    description = TextAreaField('Description: ')