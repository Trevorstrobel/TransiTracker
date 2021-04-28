Author:           	Trevor Strobel
Date:             	4/7/2021
Updated:			        4/27/2021

**Note:** For the User Manual, please see the [User Manual](UserManual/UserManual.md)



This document is meant to be read from beginnig to end. Installation steps are in an order that ensures dependencies are in place before installing a package that depends on them.  


---
Server set up
---

While any modern linux installation should work, this document will assume that you are using Ubuntu 20.04 LTS or higher. As such, all install scripts will implement the ```apt``` package manager. The default shell in Ubuntu is the Bash shell. As such, all command line entries in this document are prefaced with the ```$``` character, followed by a space. Whether you decide to type the commands manually, or copy and paste, do not insert the ```$``` character or the space at the beginning of the string. 

<h4>Python3</h4>

The TransiTracker application is written primarily in Python3 and leverages several Python3 packages to deliver a smooth experience and clean user interface. 

Note: This documentation will refer to Python3 as Python from here on. However, in the command line, it is imperitive that ```python3``` be used as ```python``` refers to Python v. 2.

First, lets make sure Python is installed. You can check the version of Python that's installed with the following command:

```
$ python3 --version
```

The returned line should look something like:
```
$ Python 3.8.5
```


If you do not have python3 installed, you may install it with the following command:

```
$ sudo apt install python3
```

<h4>pip - The Python Package Installer</h4>

Now that Python is installed, we need to install pip. pip is used to install packages that can be used by Python. Install pip with the following command:

```
$ sudo apt install python3-pip
```

With pip installed, we can move on to the next dependency. 


<h4>PostgreSQL</h4>

PostgreSQL is an extermely popular and reliable relational database. TransiTracker usus PostgreSQL to store the inventory, employee, and account data. To install the latest version of PostgreSQL, run the following commands:


First we add the PostgreSQL repository to the list of sources in our linux installation.
```
$ sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
```

Next we import the repositor signing key:

```
$ wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
```

Then we update the package lists (note the ```apt-get``` here)
```
$ sudo apt-get update
```

Finally, we install the latest version of PostgreSQL:

```
$ sudo apt-get -y install postgresql
```

<h4>pip Requirements</h4>

As mentioned previously, this application leverages several Python packages. To install those packages, navigate within the ```TransiTracker``` directory and run the following command.

```
$ pip3 install -r requirements.txt
```

**TODO: Recieved an error: launchpadlib 1.10.13 requires testresources, which is not installed. Do we need it?**


---
TransiTracker DB Generation
---


This document describes the process of (re)creating the database and tables used in
TransiTracker. This document assumes that you've already installed PostgreSQL on your linux
system. 

<h4>Database Creation</h4>

```
$ sudo -u postgres psql 
```
You will now see your prompt with the prefix ```postgres=#``` 
Note here, that each line ends with ```;```
sudo -r
First we create the databse:
```
create database transitracker_dev;
```

Then we create a user:
```
create user ttadmin with encrypted password 'csci4230';
```

Then we grant privileges to that user:
```
grant all privileges on database transitracker_dev to ttadmin;
```

Finally, we quit ```psql```:
```
\q 
```

You should now be back at your shell, indicated by the ```$ ``` character in Bash.




---
Running the Application
---
**For Devs:**To run the application in developer mode, run the following command:

```
$ python3 run.py
```



**Author Notes:** 
 Create run script for pm2. Write instructions on how to run that script. We also need to set params for running in production mode, and set the port to 80.
