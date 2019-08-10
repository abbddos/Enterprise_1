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
  usertype VARCHAR(100),
  status VARCHAR(10)
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
  category VARCHAR(50)
);

CREATE TABLE packages(
  id SERIAL PRIMARY KEY,
  packagecode VARCHAR(20),
  packagename VARCHAR(50),
  itemcode VARCHAR(50),
  itemname VARCHAR(50),
  unit VARCHAR(10),
  quantity REAL,
  description TEXT
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
	transid VARCHAR(25),
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

-- addition of foreign keys...
-- addition of foreign keys for logistics.
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

-- Creation of Admin user with superuser role, login and password 'admin'
INSERT INTO users(username, password, usertype) VALUES('admin','admin','Admin');
CREATE ROLE Admin WITH SUPERUSER LOGIN PASSWORD 'admin';

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

CREATE OR REPLACE FUNCTION updatetransaction(transid_ character varying, updateby character varying, newstatus character varying)
RETURNS void AS $$
LANGUAGE plpgsql
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

CREATE OR REPLACE VIEW Bins_view AS
SELECT bins.warehouse, bins.code, bins.status, inventory.itemcode, inventory.itemname, inventory.unit, inventory.quantity FROM bins LEFT OUTER JOIN inventory ON inventory.bin = bins.code;

