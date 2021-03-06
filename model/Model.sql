-- Creation of Database and switching to use it
-- using postgresql dialect.
CREATE DATABASE enterprise;
\c enterprise;


-- Creation of users table.
CREATE TABLE users(
  id SERIAL PRIMARY KEY,
  firstname VARCHAR(50),
  lastname VARCHAR(50),
  username VARCHAR(50) UNIQUE,
  password VARCHAR(500),
  company VARCHAR(100),
  position VARCHAR(50),
  department VARCHAR(50),
  email VARCHAR(50),
  phone1 VARCHAR(50),
  phone2 VARCHAR(50),
  usertype VARCHAR(100)[],
  status VARCHAR(10) Default 'Active'
);

CREATE TABLE approvers(
	line SERIAL PRIMARY KEY,
	firstname VARCHAR(50),
  	lastname VARCHAR(50),
  	username VARCHAR(50),
	position VARCHAR(50),
  	department VARCHAR(50),
  	email VARCHAR(50),
	Can_Approve VARCHAR(50)
);

-- Company/Organization profile:

CREATE TABLE CompanyProfile(
	id SERIAL PRIMARY KEY,
	CompanyName VARCHAR(1000),
	Address VARCHAR(50),
	phone_1 VARCHAR(20),
	phone_2 VARCHAR(20),
	email VARCHAR(50),
	pobox VARCHAR(10),
	registration VARCHAR(10),
	description TEXT
);

INSERT INTO CompanyProfile(CompanyName, Address, phone_1, phone_2, email, pobox, registration, description) VALUES('','','','','','','','');

-- Creation of logistics tables...
CREATE TABLE providers(
	id SERIAL NOT NULL PRIMARY KEY,
	name VARCHAR(50) UNIQUE,
	address VARCHAR(50),
	phone_1 VARCHAR(20),
	phone_2 VARCHAR(20),
	email VARCHAR(50),
	pobox VARCHAR(10),
	description varchar(2000)
);

CREATE TABLE grp(
  id SERIAL PRIMARY KEY,
  groupname VARCHAR(100) UNIQUE,
  description TEXT
);

CREATE TABLE items(
  id SERIAL PRIMARY KEY,
  code VARCHAR(20) UNIQUE,
  item VARCHAR(50),
  brand VARCHAR(10),
  provider VARCHAR(50),
  unit VARCHAR(5),
  unit_price REAL,
  unit_cost REAL,
  description TEXT,
  size VARCHAR(5),
  color VARCHAR(10),
  sku VARCHAR(25),
  part_number VARCHAR(25),
  ieme VARCHAR(25),
  lengh REAL,
  width REAL,
  height REAL,
  diameter REAL,
  l_unit VARCHAR(10),
  w_unit VARCHAR(10),
  h_unit VARCHAR(10),
  d_unit VARCHAR(10),
  grp VARCHAR(50),
  category VARCHAR(50),
  secondaryunit VARCHAR(10)
);

CREATE TABLE SecondaryUnits(
	Name VARCHAR(25),
	Code VARCHAR(10) PRIMARY KEY,
	Unit VARCHAR(5),
	Measure REAL
);

CREATE TABLE packages(
  id SERIAL PRIMARY KEY,
  packagecode VARCHAR(20),
  packagename VARCHAR(50),
  itemcode VARCHAR(50),
  itemname VARCHAR(50),
  unit VARCHAR(10),
  quantity REAL,
  description TEXT, 
  unit_price REAL, 
  unit_cost REAL
);

CREATE TABLE warehouses(
  id SERIAL PRIMARY KEY,
  location VARCHAR(50),
  code VARCHAR(100) UNIQUE,
  name VARCHAR(100),
  description TEXT
);

CREATE TABLE bins(
  id SERIAL PRIMARY KEY,
  code VARCHAR(50) UNIQUE,
  name VARCHAR(100),
  warehouse VARCHAR(100),
  description TEXT,
  status VARCHAR(10)
);

CREATE TABLE Transactions(
	ID SERIAL NOT NULL PRIMARY KEY,
	CreatedOn DATE,
	CreatedBy VARCHAR(50),
	EditedOn DATE,
	EditedBy VARCHAR(50),
	Type VARCHAR(10),
	ItemCode VARCHAR(20),
	ItemName VARCHAR(50),
	Warehouse VARCHAR(100),
	Bin VARCHAR(100),
	Unit VARCHAR(5),
	Quantity REAL,
	Status VARCHAR(15),
	transid VARCHAR(25),
	Comments TEXT,
	Reference VARCHAR(50)
);

CREATE TABLE Request(
	ID SERIAL NOT NULL PRIMARY KEY,
	RqstId VARCHAR(25),
	CreatedOn DATE,
	CreatedBy VARCHAR(50),
	EditedOn DATE,
	EditedBy VARCHAR(50),
	Type VARCHAR(10),
	ItemCode VARCHAR(20),
	ItemName VARCHAR(50),
	Unit VARCHAR(5),
	Quantity REAL,
	Status VARCHAR(15),
	Comments TEXT, 
	approver VARCHAR(50)
);


CREATE TABLE Inventory(
	Line SERIAL NOT NULL PRIMARY KEY,
	ItemCode VARCHAR(20),
	ItemName VARCHAR(50),
	Warehouse VARCHAR(100),
	Bin VARCHAR(100),
	Unit VARCHAR(5),
	Quantity REAL,
	lastUpdate DATE,
	UnitPrice REAL,
	BulkPrice REAL
);

-- Creating accounting tables...
CREATE TABLE Categories(
	CategoryId SERIAL NOT NULL PRIMARY KEY,
	CategoryName VARCHAR(100) UNIQUE,
	CategoryType VARCHAR(100),
	Description TEXT
);

CREATE TABLE Accounts(
	AccountID SERIAL NOT NULL PRIMARY KEY,
	AccountType VARCHAR(25),        
	AccountCategory VARCHAR(100),
	AccountName VARCHAR(100) UNIQUE,
	Currency VARCHAR(5),
	OpeningBalance REAL,
	CurrentBalance REAL,
	Comments TEXT,
	AccountCode VARCHAR(25)
);

CREATE TABLE Journal(
	EntryID SERIAL NOT NULL PRIMARY KEY,
	EntryDate DATE,
	AccountType VARCHAR(25),
	AccountCategory VARCHAR(100),
	AccountName VARCHAR(100),
	Currency VARCHAR(5),
	Debit REAL,
	Credit REAL,
	CreatedBy VARCHAR(50),
	CreatedOn DATE,
	Comments TEXT,
	EntryCode VARCHAR(25),
	Forex REAL
);

CREATE TABLE Ledger(
	entryid SERIAL NOT NULL PRIMARY KEY,
	entrydate  DATE,
	AccountType VARCHAR(25),
	AccountCategory VARCHAR(100),
	AccountName VARCHAR(100),
	BalanceAtDate REAL
);



CREATE TABLE Currency(
CurrencyID SERIAL NOT NULL PRIMARY KEY,
CurrencyName VARCHAR(25),
CurrencyCode VARCHAR(5),
ExchangeRate REAL,
FunctionalCurrency VARCHAR(3)
);

-- Invoices & bills module utilizes the same tables in Logistics module...
-- in addition to the following tables:

CREATE TABLE customers(
	id SERIAL NOT NULL PRIMARY KEY,
	name VARCHAR(50) UNIQUE,
	address VARCHAR(50),
	phone_1 VARCHAR(20),
	phone_2 VARCHAR(20),
	email VARCHAR(50),
	pobox VARCHAR(10),
	description varchar(2000)
);

CREATE TABLE Services(
	serviceid SERIAL PRIMARY KEY,
	ServiceName VARCHAR(50),
	ServiceType VARCHAR(25),
	ServiceCost REAL,
	ServicePrice REAL,
	Description TEXT
);

CREATE TABLE Invoices(
    invoiceid SERIAL NOT NULL PRIMARY KEY,
    invoicetype VARCHAR(20),
	invoicecode VARCHAR(50),
	created_by VARCHAR(50),
    sentto VARCHAR(50),
	invoicedate DATE,
    currency VARCHAR(5),
    terms VARCHAR(2000),
    description VARCHAR(50),
	unitprice REAL,
	quantity REAL,
	lineamount REAL,
	ammountsum REAL,
	discount REAL,
	tax REAL,
	totalamount REAL,
    paymentmethod VARCHAR(20),
	paymentaccount VARCHAR(100),
	invstatus VARCHAR(10) DEFAULT 'pending',
    comments TEXT
);


CREATE TABLE Bills(
	BillID SERIAL NOT NULL PRIMARY KEY,
	BillCode VARCHAR(25),
	BillDate DATE,
	BillType VARCHAR(10),
	AccountType VARCHAR(25),
	AccountCategory VARCHAR(100),
	AccountName VARCHAR(100),
	Currency VARCHAR(5),
	Debit REAL,
	Credit REAL,
	CreatedBy VARCHAR(50),
	Description TEXT,
	Comments TEXT, 
	status VARCHAR(10) DEFAULT 'Pending'
);


-- Adding Default Currencies...
INSERT INTO Currency(CurrencyName, CurrencyCode) VALUES('US Dollars', 'USD');
INSERT INTO Currency(CurrencyName, CurrencyCode) VALUES('Euro', 'EUR');
INSERT INTO Currency(CurrencyName, CurrencyCode) VALUES('Syrian Pound', 'SYP');

-- Creating basic accounting module...
INSERT INTO categories(CategoryName, CategoryType) VALUES
('Cash', 'Assets'),
('Bank Accounts', 'Assets'),
('Credit Card Accounts', 'Assets'),
('Accounts Receivable', 'Assets'),
('Inventory','Assets'),
('Land','Assets'),
('Buildings','Assets'),
('Equipment','Assets'),
('Capital','Equities'),
('Notes Payable','Liabilities'),
('Accounts Payable','Liabilities'),
('Salaries Payable','Liabilities'),
('Interest Payable','Liabilities'),
('Sales Revenues','Revenues'),
('Services Revenues', 'Revenues'),
('Interest Revenues','Revenues'),
('Salaries Expenses','Expenses'),
('Wages','Expenses'),
('Supplies','Expenses'),
('Services Expenses', 'Expenses'),
('Taxes','Expenses'),
('Cost of Goods Sold','Expenses'),
('Capital Draws','Dividends');

-- addition of foreign keys...

 --addition of foreign keys for logistics.
ALTER TABLE approvers ADD FOREIGN KEY(username) REFERENCES users(username);
ALTER TABLE items ADD FOREIGN KEY(provider) REFERENCES providers(name);
ALTER TABLE items ADD FOREIGN KEY(grp) REFERENCES grp(groupname);
ALTER TABLE packages ADD FOREIGN KEY(itemcode) REFERENCES items(code);
ALTER TABLE bins ADD FOREIGN KEY(warehouse) REFERENCES warehouses(code);
ALTER TABLE Transactions ADD FOREIGN KEY(createdby) REFERENCES users(username);
ALTER TABLE Transactions ADD FOREIGN KEY(editedby) REFERENCES users(username);
ALTER TABLE Transactions ADD FOREIGN KEY(warehouse) REFERENCES Warehouses(code);
ALTER TABLE Transactions ADD FOREIGN KEY(bin) REFERENCES bins(code);
ALTER TABLE Inventory ADD FOREIGN KEY(ItemCode) REFERENCES Items(code);
ALTER TABLE Inventory ADD FOREIGN KEY(warehouse) REFERENCES Warehouses(code);
ALTER TABLE Inventory ADD FOREIGN KEY(bin) REFERENCES Bins(code);
ALTER TABLE Request ADD FOREIGN KEY(Createdby) REFERENCES users(username);
ALTER TABLE Request ADD FOREIGN KEY(Editedby) REFERENCES users(username);
ALTER TABLE items ADD FOREIGN KEY(secondaryunit) REFERENCES SecondaryUnits(code);


--Creation of accounting tables foreign keys...

ALTER TABLE Journal ADD FOREIGN KEY(AccountType) REFERENCES Accounts(AccountType);
ALTER TABLE Journal ADD FOREIGN KEY(AccountCategory) REFERENCES Categories(CategoryName) ON UPDATE CASCADE;
ALTER TABLE Journal ADD FOREIGN KEY(AccountName) REFERENCES Accounts(AccountName);
ALTER TABLE Journal ADD FOREIGN KEY(CreatedBy) REFERENCES users(username);
ALTER TABLE Journal ADD FOREIGN KEY(AdjustedBy) REFERENCES users(username);
ALTER TABLE CashAccount ADD FOREIGN KEY(CreatedBy) REFERENCES users(username);
ALTER TABLE Ledger ADD FOREIGN KEY(AccountCategory) REFERENCES Categories(CategoryName) ON UPDATE CASCADE
ALTER TABLE accounts ADD FOREIGN KEY(accountcategory) REFERENCES categories(categoryname) ON UPDATE CASCADE;
ALTER TABLE ledger ADD FOREIGN KEY(accountname) REFERENCES accounts(accountname) ON UPDATE CASCADE;
ALTER TABLE journal ADD FOREIGN KEY(accountname) REFERENCES accounts(accountname) ON UPDATE CASCADE;


-- Creation of Admin user with superuser role, login and password 'admin'
INSERT INTO users(username, password, usertype) VALUES('admin','admin','{"root"}');
CREATE ROLE admin WITH SUPERUSER LOGIN PASSWORD 'admin';

CREATE OR REPLACE FUNCTION Inbound(transid_ VARCHAR, creator_ VARCHAR, item_name_ VARCHAR, item_code_ VARCHAR, warehouse_ VARCHAR, bin_ VARCHAR, unit_ VARCHAR, quantity_ REAL, status_ VARCHAR)
RETURNS VOID AS $$
DECLARE
	BinStatus VARCHAR;
	Unit_Price_ REAL;
	Bulk_Price_ REAL;
BEGIN
	SELECT unit_price INTO Unit_Price_ FROM Items WHERE code = item_code_;
	SELECT status INTO BinStatus FROM Bins WHERE Code  = bin_;
	IF BinStatus = 'Locked' THEN RAISE NOTICE 'Unable to perform transaction on a locked bin.';
	ELSE
		IF status_ = 'Complete' THEN
			INSERT INTO transactions(CreatedOn, CreatedBy, Type, ItemCode, ItemName, warehouse, bin, unit, quantity, status, transid) VALUES(Now(), creator_, 'Inbound',  item_code_, item_name_, warehouse_, bin_, unit_, quantity_, status_, transid_);
			IF EXISTS(SELECT Line FROM Inventory WHERE Bin  = bin_ and ItemCode = item_code_) THEN
				UPDATE Inventory SET Quantity = Quantity + quantity_, BulkPrice = BulkPrice + (Unit_Price_ * quantity_) , lastUpdate  = Now() WHERE Bin = bin_ and ItemCode = item_code_ ;
			END IF;
			IF NOT EXISTS(SELECT Line FROM Inventory WHERE Bin  = bin_ and ItemCode = item_code_) THEN
				INSERT INTO Inventory(ItemCode, ItemName, Warehouse, Bin, Unit, Quantity, lastUpdate, UnitPrice, BulkPrice) VALUES(item_code_, item_name_, warehouse_, bin_, unit_, quantity_, Now(), Unit_Price_, Unit_Price_ * quantity_);
			END IF;
		END IF;
		IF status_ = 'Pending' THEN INSERT INTO transactions(CreatedOn, CreatedBy, Type, ItemCode, ItemName, warehouse, bin, unit, quantity, status, transid) VALUES(Now(), creator_, 'Inbound',  item_code_, item_name_, warehouse_, bin_, unit_, quantity_, status_, transid_);
		UPDATE Bins SET status  = 'Locked' WHERE Code = bin_;
		END IF;
		IF status_ = 'Canceled' THEN RAISE NOTICE 'Unable to create a Cenceled transaction!!'; END IF;
	END IF;
END;
$$ LANGUAGE plpgsql;


--=====================================================================================================================================


CREATE OR REPLACE FUNCTION Outbound(transid_ VARCHAR, creator_ VARCHAR, item_name_ VARCHAR, item_code_ VARCHAR, warehouse_ VARCHAR, bin_ VARCHAR, unit_ VARCHAR, quantity_ real, status_ VARCHAR)
RETURNS VOID AS $$
DECLARE
	qty REAL;
	BinStatus VARCHAR;
	Unit_Price_ REAL;
	Bulk_Price_ REAL;
BEGIN
 SELECT unit_price INTO Unit_Price_ FROM Items WHERE Code = Item_Code_;
 SELECT quantity INTO qty FROM Inventory WHERE ItemName = item_name_;
 IF qty < quantity_ THEN
 	RAISE NOTICE 'Not enough storred quantity, can not proceed with outbout transaction.';
 ELSE
 SELECT Status INTO BinStatus FROM Bins WHERE Code  = bin_;
 IF BinStatus = 'Locked' THEN RAISE NOTICE 'Unable to perform transaction on a locked bin.';
 ELSE
	 IF status_ = 'Complete' THEN
	 	INSERT INTO transactions(CreatedOn, CreatedBy, Type, ItemCode, ItemName, warehouse, bin, unit, quantity, status, transid) VALUES(Now(), creator_, 'Outbound', item_code_, item_name_, warehouse_, bin_, unit_, quantity_, status_, transid_);
		IF EXISTS(SELECT Line FROM Inventory WHERE Bin  = bin_ and ItemCode = item_code_) THEN
			UPDATE Inventory SET Quantity = qty - quantity_ , BulkPrice = BulkPrice - (Unit_Price_ * quantity_), lastUpdate  = Now() WHERE Bin = bin_ and ItemCode = item_code_ ;
		END IF;
		IF NOT EXISTS(SELECT Line FROM Inventory WHERE Bin  = bin_ and ItemCode = item_code_) THEN
			RAISE NOTICE 'Not enough storred quantity, can not proceed with outbout transaction.';
		END IF;
	END IF;
	 IF status_ = 'Pending' THEN INSERT INTO transactions(CreatedOn, CreatedBy, Type, ItemCode, ItemName, warehouse, bin, unit, quantity, status, transid) VALUES(Now(), creator_, 'Outbound',  item_code_, item_name_,warehouse_, bin_, unit_, quantity_, status_, transid_);
	 UPDATE Bins SET status  = 'Locked' WHERE Code = bin_;
	 END IF;
	 IF status_ = 'Canceled' THEN RAISE NOTICE 'Unable to create a Cenceled transaction!!'; END IF;
 END IF;
END IF;
END;
$$ LANGUAGE plpgsql;

--=====================================================================================================================================

CREATE OR REPLACE FUNCTION updatetransaction(transid_ VARCHAR, updateby VARCHAR, newstatus VARCHAR)
RETURNS void AS $$

DECLARE
	rec RECORD;
	unitprice_ REAL;
BEGIN
	FOR rec IN SELECT * FROM transactions WHERE transid = transid_ LOOP
		SELECT unit_price INTO unitprice_ FROM items WHERE code = rec.itemcode;
		IF newstatus = 'Complete' THEN
			UPDATE transactions SET editedon = now(), editedby = updateby, status = newstatus WHERE id = rec.id;
			IF rec.type = 'Inbound' THEN
				IF EXISTS(SELECT line FROM Inventory WHERE Bin = rec.Bin AND Itemcode = rec.Itemcode) THEN
					UPDATE inventory SET quantity = quantity + rec.quantity, BulkPrice = BulkPrice + (unitprice_ * rec.quantity), lastupdate = now() WHERE bin = rec.bin AND ItemCode = rec.Itemcode;
				END IF;
				IF NOT EXISTS(SELECT line FROM Inventory WHERE Bin = rec.Bin AND Itemcode = rec.Itemcode) THEN
					INSERT INTO inventory(ItemCode, ItemName, Warehouse, Bin, Unit, Quantity, lastUpdate, UnitPrice, BulkPrice) VALUES(rec.itemcode, rec.itemname, rec.warehouse, rec.bin, rec.unit, rec.quantity, now(), unitprice_, unitprice_ * rec.quantity);
				END IF;
			END IF;
			IF rec.type = 'Outbound' THEN
				IF EXISTS(SELECT line FROM Inventory WHERE Bin = rec.Bin AND Itemcode = rec.Itemcode) THEN
					UPDATE inventory SET quantity = quantity - rec.quantity, BulkPrice = BulkPrice + (unitprice_ * rec.quantity), lastupdate = now() WHERE bin = rec.bin AND ItemCode = rec.Itemcode;
				END IF;
				IF NOT EXISTS(SELECT line FROM Inventory WHERE Bin = rec.Bin AND Itemcode = rec.Itemcode) THEN
					RAISE NOTICE 'Not enough storred quantity, can not proceed with outbout transaction.';
				END IF;
			END IF;
			UPDATE bins SET status = 'Open' WHERE code = rec.bin;
		END IF;

		IF newstatus = 'Canceled' THEN
			UPDATE transactions SET editedon = now(), editedby = updateby, status = newstatus WHERE id = rec.id;
			UPDATE bins SET status = 'Open' WHERE code = rec.bin;
		END IF;
	END LOOP;
END;
$$ LANGUAGE plpgsql;

--===============================================================================================================================================================

CREATE OR REPLACE FUNCTION CreateJournalEntry(jrncode VARCHAR, accttype VARCHAR, acctcat VARCHAR, acctname VARCHAR, crncy VARCHAR, dbt REAL, cdt REAL, createdby_ VARCHAR, comnts TEXT)
RETURNS void AS $$
DECLARE
	ex_rate REAL;
	CB REAL;
BEGIN
	SELECT exchangerate INTO ex_rate FROM Currency WHERE currencycode = crncy;
	SELECT CurrentBalance INTO CB FROM Accounts WHERE AccountName = acctname;
	INSERT INTO Journal(EntryDate, AccountType, AccountCategory, AccountName, Currency, Debit, Credit, CreatedOn, CreatedBy, Comments, entrycode, Forex) VALUES(current_date, accttype, acctcat, acctname, crncy, dbt * ex_rate, cdt * ex_rate, now(), createdby_, comnts, jrncode, ex_rate);
	IF accttype = 'Assets' OR accttype = 'Expenses' OR accttype = 'Dividends' THEN
		UPDATE Accounts SET CurrentBalance = CurrentBalance + (dbt * ex_rate) - (cdt * ex_rate) WHERE AccountName = acctname;
		IF EXISTS(SELECT * FROM Ledger WHERE accountname = acctname AND entrydate = current_date) THEN
			UPDATE Ledger SET BalanceAtDate = CB + (dbt * ex_rate) - (cdt * ex_rate) WHERE AccountName = acctname;
		END IF;
		IF NOT EXISTS(SELECT * FROM Ledger WHERE AccountName = acctname AND entrydate = current_date) THEN
			INSERT INTO Ledger(entrydate, accounttype, accountcategory, accountname, BalanceAtDate) VALUES(current_date,accttype, acctcat, acctname, CB + (dbt * ex_rate) - (cdt * ex_rate));
		END IF;
	END IF;
	IF accttype = 'Equities' OR accttype = 'Liabilities' OR accttype = 'Revenues' THEN
		UPDATE Accounts SET CurrentBalance = CurrentBalance - (dbt * ex_rate) + (cdt * ex_rate) WHERE AccountName = acctname;
		IF EXISTS(SELECT * FROM Ledger WHERE accountname = acctname AND entrydate = current_date) THEN
			UPDATE Ledger SET BalanceAtDate = CB - (dbt * ex_rate) + (cdt * ex_rate) WHERE AccountName = acctname;
		END IF;
		IF NOT EXISTS(SELECT * FROM Ledger WHERE accountname = acctname AND entrydate = current_date) THEN
			INSERT INTO Ledger(entrydate, accounttype, accountcategory, accountname, BalanceAtDate) VALUES(current_date,accttype, acctcat, acctname,CB - (dbt * ex_rate) + (cdt * ex_rate));
		END IF;
	END IF;
END;
$$ LANGUAGE plpgsql;

--===============================================================================================================================================================
CREATE OR REPLACE FUNCTION GetDebitCreditTotals(entrycode_ VARCHAR)
RETURNS TABLE(
	record_debit REAL,
	record_credit REAL
) AS $$

BEGIN
	RETURN QUERY SELECT SUM(Debit) , SUM(Credit)  FROM journal WHERE entrycode = entrycode_ GROUP BY entrycode;

END;
$$ LANGUAGE plpgsql;


--===============================================================================================================================================================

CREATE OR REPLACE FUNCTION CreateAccount(account VARCHAR, category VARCHAR, code VARCHAR, name VARCHAR, currency_ VARCHAR, OBalance REAL, CBalance REAL, comments TEXT)
RETURNS void AS $$
DECLARE 
	ex_rate REAL;

BEGIN
	SELECT exchangerate INTO ex_rate FROM Currency WHERE currencycode = currency_;
	INSERT INTO accounts(accounttype, accountcategory, accountname, currency, openingbalance, currentbalance, comments, accountcode) VALUES(account, category, name, currency_, OBalance, CBalance * ex_rate, comments, code);
	INSERT INTO ledger(entrydate, accounttype, accountcategory, accountname, BalanceAtDate) VALUES(current_date, account, category, name, CBalance * ex_rate); 
END;
$$ LANGUAGE plpgsql;

--===============================================================================================================================================================

CREATE OR REPLACE FUNCTION UpdateAccount(ident INT, account VARCHAR, category VARCHAR, newcode VARCHAR, name VARCHAR, currency_ VARCHAR, OBalance REAL, CBalance REAL, comments_ TEXT)
RETURNS void AS $$
DECLARE
	ex_rate REAL;
	
BEGIN
	SELECT exchangerate INTO ex_rate FROM Currency WHERE currencycode = currency_;
	IF NOT EXISTS(SELECT * FROM ledger WHERE accountname = name AND entrydate = current_date) THEN
		UPDATE ACCOUNTS set AccountType = account, AccountCategory = category, AccountCode = newcode, AccountName = name, Currency = currency_, OpeningBalance = OBalance, CurrentBalance = CBalance * ex_rate, Comments = comments_ WHERE AccountID = ident;
		INSERT INTO ledger(entrydate, accounttype, accountcategory, accountname, BalanceAtDate) VALUES(current_date, account, category, name, CBalance * ex_rate);
	END IF;
	IF EXISTS(SELECT * FROM ledger WHERE accountname = name AND entrydate = current_date) THEN
		UPDATE ACCOUNTS set AccountType = account, AccountCategory = category, AccountCode = newcode,  Currency = currency_, OpeningBalance = OBalance, CurrentBalance = CBalance * ex_rate, Comments = comments_ WHERE AccountID = ident;
		UPDATE ledger SET balanceatdate = CBalance * ex_rate WHERE accountname = name AND entrydate = current_date;
	END IF;
END;
$$ LANGUAGE plpgsql;

--===============================================================================================================================================================

CREATE OR REPLACE FUNCTION Balance_sheet(acttype VARCHAR, entry DATE)
RETURNS TABLE(
    
	name VARCHAR,
	balance REAL,
	entrdate DATE,
	type VARCHAR
) AS $$ 

BEGIN
	RETURN QUERY SELECT DISTINCT ON (accountname) accountname, balanceatdate, entrydate, accounttype FROM  ledger WHERE entrydate <= entry AND accounttype = acttype ORDER BY accountname, entrydate DESC;
END;
$$ LANGUAGE plpgsql;

--===============================================================================================================================================================
CREATE OR REPLACE FUNCTION CreateItem(code_ VARCHAR, item_ VARCHAR, brand_ VARCHAR, provider_ VARCHAR, unit_ VARCHAR, unitprice_ REAL, unitcost_ REAL, description_ TEXT, size_ VARCHAR, color_ VARCHAR, sku_ VARCHAR, part_number_ VARCHAR, ieme_ VARCHAR, length_ REAL, width_ REAL, height_ REAL, diameter_ REAL, l_unit_ VARCHAR, w_unit_ VARCHAR, h_unit_ VARCHAR, d_unit_ VARCHAR, grp_ VARCHAR, category_ VARCHAR, secondaryunit_ VARCHAR)
RETURNS VOID AS $$
DECLARE
   Cur VARCHAR;
BEGIN
	INSERT INTO items(code, item, brand, provider, unit, unit_price, unit_cost, description, size, color, sku, part_number, ieme, lengh, width, height, diameter, l_unit, w_unit, h_unit, d_unit, grp, category, secondaryunit) VALUES(code_, item_, brand_, provider_, unit_, unitprice_, unitcost_, description_, size_, color_, sku_, part_number_, ieme_, length_, width_, height_, diameter_, l_unit_, w_unit_, h_unit_, d_unit_, grp_, category_, secondaryunit_);
	SELECT currencycode INTO Cur FROM Currency WHERE FunctionalCurrency = 'Yes';
	-- When item is identified as Asset, create category 'inventory' under Assets if it does not exist and create item as asset account.
	IF category_ = 'Asset' THEN
		INSERT INTO categories(categoryname, categorytype) select 'Inventory','Assets' where not exists(select categoryname from categories where categoryname = 'Inventory');
		PERFORM CreateAccount('Assets','Inventory','Custom_Code' ,item_, Cur, 0,0, '');

	END IF;

	-- When item is not identified as asset, create category 'Supplies' under Expenses if it does not exist and create item as expense account.
	IF category_ = 'Non-Asset' THEN
		INSERT INTO categories(categoryname, categorytype) select 'Supplies','Expenses' where not exists(select categoryname from categories where categoryname = 'Supplies');
		PERFORM CreateAccount('Expenses','Supplies','Custom_Code' ,item_, Cur, 0,0, '');
	END IF;
END;
$$ LANGUAGE plpgsql;

--===============================================================================================================================================================

CREATE OR REPLACE FUNCTION UpdateItem(itm INT, itemname VARCHAR, brand_ VARCHAR, provider_ VARCHAR, unit_ VARCHAR, uprice REAL, ucost REAL, description_ TEXT, size_ VARCHAR, color_ VARCHAR, sku_ VARCHAR, partnum VARCHAR, ieme_ VARCHAR, length_ REAL, width_ REAL, height_ REAL, diameter_ REAL, lunit VARCHAR, wunit VARCHAR, hunit VARCHAR, dunit VARCHAR, grp_ VARCHAR, category_ VARCHAR, secondaryunit_ VARCHAR)
RETURNS VOID AS $$
DECLARE
	X VARCHAR;
BEGIN
	SELECT item INTO X FROM items WHERE id = itm;
	UPDATE items SET Item = itemname, Brand = brand_, Provider = provider_, Unit = unit_, Unit_Price = uprice, unit_cost = ucost, Description = description_ , Size = size_, Color = color_, sku = sku_, part_number = partnum, ieme = ieme_, lengh = length_, width = width_ , height = height_, diameter = diameter_, l_unit = lunit, w_unit = wunit, h_unit = hunit, d_unit = dunit, grp = grp_, category = category_ , secondaryunit = secondaryunit_ WHERE id = itm;
	IF category_ = 'Asset' THEN
		UPDATE Accounts SET Accounttype = 'Assets', AccountCategory = 'Inventory', AccountCode = 'Custom_Code' WHERE AccountName = X;
		UPDATE ledger SET Accounttype = 'Assets', AccountCategory = 'Inventory' WHERE AccountName = X;
	END IF;
	IF category_ = 'Non-Asset' THEN
		UPDATE Accounts SET Accounttype = 'Expenses', AccountCategory = 'Supplies', AccountCode = 'Custom_Code' WHERE AccountName = X;
		UPDATE ledger SET Accounttype = 'Expenses', AccountCategory = 'Supplies' WHERE AccountName = X;
	END IF;
END;
$$ LANGUAGE plpgsql;

--===============================================================================================================================================================

CREATE OR REPLACE FUNCTION CreateProvider(name_ VARCHAR, address_ VARCHAR, phone1_ VARCHAR, phone2_ VARCHAR, email_ VARCHAR, pobox_ VARCHAR, description_ VARCHAR)
RETURNS VOID AS $$
DECLARE
   Cur VARCHAR;
BEGIN
	SELECT currencycode INTO Cur FROM Currency WHERE FunctionalCurrency = 'Yes';
	INSERT INTO providers(name, address, phone_1, phone_2, email, pobox, description) VALUES(name_, address_, phone1_, phone2_, email_, pobox_, description_);
	INSERT INTO categories(categoryname, categorytype) select 'Accounts Payable','Liabilities' where not exists(select categoryname from categories where categoryname = 'Accounts Payable');
	PERFORM CreateAccount('Liabilities','Accounts Payable','Custom_Code' ,name_, Cur, 0,0, '');
END;
$$ LANGUAGE plpgsql;

--===============================================================================================================================================================

CREATE OR REPLACE FUNCTION CreateCustomer(name_ VARCHAR, address_ VARCHAR, phone1_ VARCHAR, phone2_ VARCHAR, email_ VARCHAR, pobox_ VARCHAR, description_ VARCHAR)
RETURNS VOID AS $$
DECLARE
   Cur VARCHAR;
BEGIN
	SELECT currencycode INTO Cur FROM Currency WHERE FunctionalCurrency = 'Yes';
	INSERT INTO customers(name, address, phone_1, phone_2, email, pobox, description) VALUES(name_, address_, phone1_, phone2_, email_, pobox_, description_);
	INSERT INTO categories(categoryname, categorytype) select 'Accounts Receivable','Assets' where not exists(select categoryname from categories where categoryname = 'Accounts Receivable');
	PERFORM CreateAccount('Assets','Accounts Receivable','Custom_Code' ,name_, Cur, 0,0, '');
END;
$$ LANGUAGE plpgsql;


--===============================================================================================================================================================

CREATE OR REPLACE FUNCTION CreateService(name_ VARCHAR, type_ VARCHAR, cost_ REAL, price_ REAL, description_ TEXT)
RETURNS VOID AS $$
DECLARE 
	Cur VARCHAR;
BEGIN
	SELECT currencycode INTO Cur FROM Currency WHERE FunctionalCurrency = 'Yes';
	INSERT INTO SERVICES(ServiceName, ServiceType, ServiceCost, ServicePrice, Description) VALUES(name_, type_, cost_, price_, description_);
	IF type_ = 'Revenue' THEN
		PERFORM CreateAccount('Revenues','Services Revenues','Custom_Code' ,name_, Cur, 0,0, '');
	END IF;
	IF type_ = 'Expense' THEN
		PERFORM CreateAccount('Expenses','Services Expenses','Custom_Code' ,name_, Cur, 0,0, '');
	END IF;
END;
$$ LANGUAGE plpgsql;

--===============================================================================================================================================================

CREATE OR REPLACE FUNCTION UpdateService(code_ INT, name_ VARCHAR, type_ VARCHAR, cost_ REAL, price_ REAL, description_ TEXT)
RETURNS VOID AS $$
DECLARE 
	S VARCHAR;
BEGIN
	SELECT ServiceName INTO S FROM Services WHERE ServiceID = code_;
	UPDATE Services SET ServiceName = name_, ServiceType = type_, ServiceCost = cost_, ServicePrice = price_, Description = description_ WHERE ServiceID = code_;
	IF type_ = 'Revenue' THEN
		UPDATE Accounts SET Accounttype = 'Revenues', AccountCategory = 'Services Revenues', AccountCode = 'Custom_Code' WHERE AccountName = S;
		UPDATE ledger SET Accounttype = 'Revenues', AccountCategory = 'Services Revenues' WHERE AccountName = S;
	END IF;
	IF type_ = 'Expense' THEN
		UPDATE Accounts SET Accounttype = 'Expenses', AccountCategory = 'Services Expenses', AccountCode = 'Custom_Code' WHERE AccountName = S;
		UPDATE ledger SET Accounttype = 'Expenses', AccountCategory = 'Services Expenses' WHERE AccountName = S;
	END IF;
END;
$$ LANGUAGE plpgsql;

--===============================================================================================================================================================

CREATE OR REPLACE FUNCTION RegisterInvoice_SRF(jrncode VARCHAR, code VARCHAR, created_by VARCHAR, SR VARCHAR, CGS VARCHAR)
RETURNS VOID AS $$
DECLARE
	term VARCHAR;
	invtype VARCHAR;
	sent_name VARCHAR;
	sent_type VARCHAR;
	sent_cat VARCHAR;
	bill_type VARCHAR;
	bill_cat VARCHAR;
	bill_name VARCHAR;
	bill_amnt REAL;
	crn VARCHAR;
	acct VARCHAR;
	cat VARCHAR;
	rec RECORD;
	amnt REAL;
	amnt_ REAL;
	ex_rate REAL;
	crn_ VARCHAR;
	ln_cost REAL;
	T_cost REAL;
	service_price REAL;
	
BEGIN
	
	
	SELECT invoicetype, sentto, terms, paymentaccount, totalamount, currency INTO invtype, sent_name, term, bill_name, bill_amnt, crn FROM invoices WHERE invoicecode = code GROUP BY invoicetype, sentto, terms, paymentaccount, totalamount, currency;
	SELECT accounttype, accountcategory INTO sent_type, sent_cat FROM accounts WHERE accountname = sent_name;
	SELECT accounttype, accountcategory INTO bill_type, bill_cat FROM accounts WHERE accountname = bill_name;
	SELECT ExchangeRate INTO ex_rate FROM currency WHERE currencycode = crn;
	

	IF 	invtype = 'sales' THEN
	T_cost = 0;
	service_price = 0;
		IF term = 'Immediate payment' THEN
			FOR rec in SELECT * FROM invoices WHERE invoicecode = code LOOP
				SELECT accounttype, accountcategory, currency INTO acct, cat, crn_ FROM accounts WHERE accountname = rec.description;
				IF NOT EXISTS(SELECT item FROM items WHERE item = rec.description) THEN
					amnt = rec.lineamount - (rec.lineamount * (rec.discount/100)) + (rec.lineamount * (rec.tax/100));
					amnt_ = amnt * ex_rate;
					service_price = service_price + amnt_;
					PERFORM CreateJournalEntry(jrncode, acct, cat, rec.description, crn_, 0, amnt_, created_by, rec.comments);
				END IF;
				IF EXISTS(SELECT item FROM items WHERE item = rec.description) THEN
					SELECT unit_cost INTO ln_cost FROM items WHERE item = rec.description; 
					amnt = rec.lineamount - (rec.lineamount * (rec.discount/100)) + (rec.lineamount * (rec.tax/100));
					amnt_ = amnt * ex_rate;
					PERFORM CreateJournalEntry(jrncode, acct, cat, rec.description, crn_, 0, ln_cost * rec.quantity, created_by, rec.comments);
					T_cost = T_cost + (ln_cost * rec.quantity);
				END IF;				
			END LOOP;

			PERFORM CreateJournalEntry(jrncode, bill_type, bill_cat, bill_name, crn, bill_amnt, 0,  created_by, '--');
			IF T_cost != 0 THEN
				PERFORM CreateJournalEntry(jrncode, 'Revenues', 'Sales Revenues', SR, crn, 0, bill_amnt - service_price, created_by, '--');
				PERFORM CreateJournalEntry(jrncode, 'Expenses', 'Cost of Goods Sold', CGS, crn, T_cost, 0, created_by, '--');
			END IF;

		END IF;
		IF term = 'Later payment' THEN
			FOR rec in SELECT * FROM invoices WHERE invoicecode = code LOOP
				SELECT accounttype, accountcategory, currency INTO acct, cat, crn_ FROM accounts WHERE accountname = rec.description;
				IF NOT EXISTS(SELECT item FROM items WHERE item = rec.description) THEN
					amnt = rec.lineamount - (rec.lineamount * (rec.discount/100)) + (rec.lineamount * (rec.tax/100));
					amnt_ = amnt * ex_rate;
					service_price = service_price + amnt_;
					PERFORM CreateJournalEntry(jrncode, acct, cat, rec.description, crn_, 0, amnt_, created_by, rec.comments);
				END IF;
				IF EXISTS(SELECT item FROM items WHERE item = rec.description) THEN
					SELECT unit_cost INTO ln_cost FROM items WHERE item = rec.description;
					amnt = rec.lineamount - (rec.lineamount * (rec.discount/100)) + (rec.lineamount * (rec.tax/100));
					amnt_ = amnt * ex_rate;
					PERFORM CreateJournalEntry(jrncode, acct, cat, rec.description, crn_, 0, ln_cost * rec.quantity, created_by, rec.comments);
					T_cost = T_cost + (ln_cost * rec.quantity);
				END IF;								
			END LOOP;
			PERFORM CreateJournalEntry(jrncode, sent_type, sent_cat, sent_name, crn, bill_amnt, 0,  created_by, '--');
			IF T_cost != 0 THEN
				PERFORM CreateJournalEntry(jrncode, 'Revenues', 'Sales Revenues', SR, crn, 0, bill_amnt - service_price, created_by, '--');
				PERFORM CreateJournalEntry(jrncode, 'Expenses', 'Cost of Goods Sold', CSG, crn, T_cost, 0, created_by, '--');
			END IF;
		END IF;
	END IF;

	IF invtype = 'refund' THEN
	T_cost = 0;
	service_price = 0;
		IF term = 'Immediate payment' THEN
			FOR rec in SELECT * FROM invoices WHERE invoicecode = code LOOP
				SELECT accounttype, accountcategory, currency INTO acct, cat, crn_ FROM accounts WHERE accountname = rec.description;
				IF NOT EXISTS(SELECT item FROM items WHERE item = rec.description) THEN
					amnt = rec.lineamount - (rec.lineamount * (rec.discount/100)) + (rec.lineamount * (rec.tax/100));
					amnt_ = amnt * ex_rate;
					service_price = service_price + amnt_;
					PERFORM CreateJournalEntry(jrncode, acct, cat, rec.description, crn_, amnt_, 0, created_by, rec.comments);
				END IF;
				IF EXISTS(SELECT item FROM items WHERE item = rec.description) THEN
					SELECT unit_cost INTO ln_cost FROM items WHERE item = rec.description;
					amnt = rec.lineamount - (rec.lineamount * (rec.discount/100)) + (rec.lineamount * (rec.tax/100));
					amnt_ = amnt * ex_rate;
					PERFORM CreateJournalEntry(jrncode, acct, cat, rec.description, crn_, ln_cost * rec.quantity, 0, created_by, rec.comments);
					T_cost = T_cost + (ln_cost * rec.quantity);
				END IF;				
			END LOOP;
			PERFORM CreateJournalEntry(jrncode, bill_type, bill_cat, bill_name, crn, 0, bill_amnt, created_by, '--');
			IF T_cost != 0 THEN
				PERFORM CreateJournalEntry(jrncode, 'Revenues', 'Sales Revenues', SR, crn, bill_amnt - service_price, 0, created_by, '--');
				PERFORM CreateJournalEntry(jrncode, 'Expenses', 'Cost of Goods Sold', CGS, crn, 0, T_cost, created_by, '--');
			END IF;
		END IF;

		IF term = 'Later payment' THEN
			FOR rec in SELECT * FROM invoices WHERE invoicecode = code LOOP
				SELECT accounttype, accountcategory, currency INTO acct, cat, crn_ FROM accounts WHERE accountname = rec.description;
				IF NOT EXISTS(SELECT item FROM items WHERE item = rec.description) THEN
					amnt = rec.lineamount - (rec.lineamount * (rec.discount/100)) + (rec.lineamount * (rec.tax/100));
					amnt_ = amnt * ex_rate;
					service_price = service_price + amnt_;
					PERFORM CreateJournalEntry(jrncode, acct, cat, rec.description, crn_, amnt_, 0, created_by, rec.comments);
				END IF;
				IF EXISTS(SELECT item FROM items WHERE item = rec.description) THEN
					SELECT unit_cost INTO ln_cost FROM items WHERE item = rec.description;
					amnt = rec.lineamount - (rec.lineamount * (rec.discount/100)) + (rec.lineamount * (rec.tax/100));
					amnt_ = amnt * ex_rate;
					PERFORM CreateJournalEntry(jrncode, acct, cat, rec.description, crn_, ln_cost * rec.quantity, 0, created_by, rec.comments);
					T_cost = T_cost + (ln_cost * rec.quantity);
				END IF;						
			END LOOP;
			PERFORM CreateJournalEntry(jrncode, sent_type, sent_cat, sent_name, crn, 0, bill_amnt, created_by, '--');
			IF T_cost != 0 THEN
				PERFORM CreateJournalEntry(jrncode, 'Revenues', 'Sales Revenues', SR, crn, bill_amnt - service_price, 0, created_by, '--');
				PERFORM CreateJournalEntry(jrncode, 'Expenses', 'Cost of Goods Sold', CGS, crn, 0, T_cost, created_by, '--');
			END IF;
		END IF;
	END IF;
END;
$$ LANGUAGE plpgsql;

--===========================================================================================================================================================

CREATE OR REPLACE FUNCTION RegisterInvoice_PRT(jrncode VARCHAR, code VARCHAR, created_by VARCHAR)
RETURNS VOID AS $$
DECLARE
	term VARCHAR;
	invtype VARCHAR;
	sent_name VARCHAR;
	sent_type VARCHAR;
	sent_cat VARCHAR;
	bill_type VARCHAR;
	bill_cat VARCHAR;
	bill_name VARCHAR;
	bill_amnt REAL;
	crn VARCHAR;
	acct VARCHAR;
	cat VARCHAR;
	rec RECORD;
	amnt REAL;
	amnt_ REAL;
	ex_rate REAL;
	crn_ VARCHAR;

BEGIN

	SELECT invoicetype, sentto, terms, paymentaccount, totalamount, currency INTO invtype, sent_name, term, bill_name, bill_amnt, crn FROM invoices WHERE invoicecode = code GROUP BY invoicetype, sentto, terms, paymentaccount, totalamount, currency;
	SELECT accounttype, accountcategory INTO sent_type, sent_cat FROM accounts WHERE accountname = sent_name;
	SELECT accounttype, accountcategory INTO bill_type, bill_cat FROM accounts WHERE accountname = bill_name;
	SELECT ExchangeRate INTO ex_rate FROM currency WHERE currencycode = crn;	

	IF invtype = 'return' THEN
		IF term = 'Immediate payment' THEN
			FOR rec in SELECT * FROM invoices WHERE invoicecode = code LOOP
				SELECT accounttype, accountcategory, currency INTO acct, cat, crn_ FROM accounts WHERE accountname = rec.description;
				amnt = rec.lineamount - (rec.lineamount * (rec.discount/100)) + (rec.lineamount * (rec.tax/100));
				amnt_ = amnt * ex_rate;
				PERFORM CreateJournalEntry(jrncode, acct, cat, rec.description, crn_, 0, amnt_, created_by, rec.comments);				
			END LOOP;
			PERFORM CreateJournalEntry(jrncode, bill_type, bill_cat, bill_name, crn, bill_amnt, 0,  created_by, '--');
		END IF;
		IF term = 'Later payment' THEN
			FOR rec in SELECT * FROM invoices WHERE invoicecode = code LOOP
				SELECT accounttype, accountcategory, currency INTO acct, cat, crn_ FROM accounts WHERE accountname = rec.description;
				amnt = rec.lineamount - (rec.lineamount * (rec.discount/100)) + (rec.lineamount * (rec.tax/100));
				amnt_ = amnt * ex_rate;
				PERFORM CreateJournalEntry(jrncode, acct, cat, rec.description, crn_, 0, amnt_, created_by, rec.comments);				
			END LOOP;
			PERFORM CreateJournalEntry(jrncode, sent_type, sent_cat, sent_name, crn, bill_amnt, 0,  created_by, '--');
		END IF;
	END IF;

	IF invtype = 'procurement' THEN
		IF term = 'Immediate payment' THEN
			FOR rec in SELECT * FROM invoices WHERE invoicecode = code LOOP
				SELECT accounttype, accountcategory, currency INTO acct, cat, crn_ FROM accounts WHERE accountname = rec.description;
				amnt = rec.lineamount - (rec.lineamount * (rec.discount/100)) + (rec.lineamount * (rec.tax/100));
				amnt_ = amnt * ex_rate;
				PERFORM CreateJournalEntry(jrncode, acct, cat, rec.description, crn_, amnt_, 0, created_by, rec.comments);				
			END LOOP;
			PERFORM CreateJournalEntry(jrncode, bill_type, bill_cat, bill_name, crn, 0, bill_amnt, created_by, '--');
		END IF;
		IF term = 'Later payment' THEN
			FOR rec in SELECT * FROM invoices WHERE invoicecode = code LOOP
				SELECT accounttype, accountcategory, currency INTO acct, cat, crn_ FROM accounts WHERE accountname = rec.description;
				amnt = rec.lineamount - (rec.lineamount * (rec.discount/100)) + (rec.lineamount * (rec.tax/100));
				amnt_ = amnt * ex_rate;
				PERFORM CreateJournalEntry(jrncode, acct, cat, rec.description, crn_, amnt_, 0, created_by, rec.comments);				
			END LOOP;
			PERFORM CreateJournalEntry(jrncode, sent_type, sent_cat, sent_name, crn, 0, bill_amnt, created_by, '--');
		END IF;
	END IF;

	
END;
$$ LANGUAGE plpgsql;
	
--===============================================================================================================================================================
CREATE OR REPLACE FUNCTION RegisterBill(billcode_ VARCHAR)
RETURNS VOID AS $$
DECLARE rec RECORD;
BEGIN
	FOR rec IN SELECT * FROM bills WHERE billcode = billcode_ LOOP
		PERFORM CreateJournalEntry(rec.billcode, rec.accounttype, rec.accountcategory, rec.accountname, rec.currency, rec.debit, rec.credit, rec.createdby, rec.description);
	END LOOP;
END;
$$ LANGUAGE plpgsql;

--===============================================================================================================================================================
-- Views...

CREATE OR REPLACE VIEW Bins_view AS	
SELECT bins.warehouse, bins.code, bins.status, inventory.itemcode, inventory.itemname, inventory.unit, inventory.quantity FROM bins LEFT OUTER JOIN inventory ON inventory.bin = bins.code;

--===============================================================================================================================================================
CREATE OR REPLACE VIEW View_Journal AS
select entrydate, entrycode, accounttype, accountcategory, accountname, currency, debit/forex as dbt, credit/forex as cdt, comments, forex from journal;

--===============================================================================================================================================================

CREATE OR REPLACE VIEW GetAccount AS
SELECT accounts.accountid, accounts.accounttype, accounts.accountcategory, accounts.accountname, accounts.currency, accounts.openingbalance, accounts.currentbalance, accounts.comments, accounts.accountcode, currency.exchangerate FROM accounts INNER JOIN currency ON accounts.currency = currency.currencycode;

--===============================================================================================================================================================

-- This is to be used while modifying the items, providers and customers insertion API...
-- INSERT INTO categories(categoryname, categorytype) select 'namevalue' 'typevalue' where not exists(select categoryname from category where categoryname = 'namevalue');
