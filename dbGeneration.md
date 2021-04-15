Author:           Trevor Strobel
Date:             4/7/2021


---
TransiTracker DB Generation
---
**Note:This document is an early draft and all elements are subject to change without notice.**

This document describes the process of (re)creating the database and tables used in
TransiTracker. This document assumes that you've already installed PostgreSQL on your linux
system. 

<h4>Database Creation</h4>

```
sudo -u postgres psql 
```
You will now see your prompt with the prefix ```postgres=#``` 
Note here, that each line ends with ```;```

```
create database transitracker_dev;
create user ttadmin with encrypted password `csci4230`;
grant all privileges on database transitracker_dev to ttadmin;

\q 
```

<h4>Item Table</h4>
The Item table describes items stocked and tracked by ECU's Transit Department.

```sql
CREATE TABLE `Item` (
	`ItemID` INT NOT NULL AUTO_INCREMENT,
	`Name` VARCHAR(50) NOT NULL COMMENT 'Product Name',
	`Current_Stock` INT COMMENT 'Number currently in stock',
	`Reorder_Threshold` INT,
	`Distributor` VARCHAR(30) COMMENT 'Where do you get this item?',
	PRIMARY KEY (`ItemID`)
);
```

<h4>Employee Table</h4>
The Employee table's entries represent an employee of ECU's Transit Department.

```sql
CREATE TABLE `Employee` (
	`EmployeeID` INT NOT NULL AUTO_INCREMENT,
	`First_Name` VARCHAR(30)  NOT NULL COMMENT 'Employee\'s' first name',
	`Last_Name` VARCHAR(30) NOT NULL COMMENT 'Employees last name',
	`PirateID` VARCHAR(40) NOT NULL COMMENT 'Employees Pirate ID. Ex: smithj21@students.ecu.edu',
	`Phone` CHAR(10) COMMENT 'Phone Number. Note: this field only accepts 10-digit US phone numbers. ',
	PRIMARY KEY (`EmployeeID`)
);
```

<h4>Transaction Table</h4>

The Transaction table's entries represent a transaction within ECU's Transit Department. A transaction occurs when a driver or other employee removes an item from inventory to be used on a vehicle, or in an office.

```sql
CREATE TABLE `Transaction` (
    `TransactionID` INT NOT NULL AUTO_INCREMENT,
    `EmployeeID` INT NOT NULL,
    `ItemID` INT NOT NULL,
    `Number` INT NOT NULL COMMENT 'Number of items taken from inventory',
    PRIMARY KEY(`TransactionID`),
    FOREIGN KEY (`EmployeeID`) REFERENCES Employee(EmployeeID),
    FOREIGN KEY (`ItemID`) REFERENCES Item(ItemID)
);
```




<h4>Login Table </h4>

```sql

CREATE TABLE `Login` (

	`Username` VARCHAR(30) NOT NULL COMMENT `Employee's log in username`,
	`Password` VARCHAR(30) NOT NULL COMMENT `Employees login password`,
	`EmployeeID` INT NOT NULL,

	PRIMARY KEY (`Username`),
	FOREIGN KEY (`EmployeeID`) REFERENCES Employee(EmployeeID)
);
```