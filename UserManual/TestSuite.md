
<h1>TransiTracker Test Suite</h1>

<h2>Test 1: General Database CRUD Functions</h2>

If you're interested in manually testing the application, follow these steps to setup your working environment

<h4>Install Python</h3>


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
<div style="page-break-after: always"></div>

<h4>pip - The Python Package Installer</h4>

Now that Python is installed, we need to install pip. pip is used to install packages that can be used by Python. Install pip with the following command:

```
$ sudo apt install python3-pip
```

<h4>factory-boy</h4>

factory_boy allows you to use objects customized for the current test, while only declaring the test-specific fields:

```
$ pip install factory_boy
```

<h4>SQLAlchemy 1.4.11</h4>

SQLAlchemy provides a full suite of well known enterprise-level persistence patterns

```
$ pip install SQLAlchemy
```

<h4>PostgreSQL</h4>

PostgreSQL is a free and open-source relational database management system.

```
$ brew install postgresql
```

<h2>Running the Test</h2>

Now that the dependencies are set, we can begin the test.

```
$ pytest database_tests.py
```

<h2>Results</h2>
If the server is established and the tests are working, the test will print the following:

```
$ Tables created successfully
```
OR it might not print anything at all.

If the server is not established, the test will output an error.

```
E       sqlalchemy.exc.OperationalError: (psycopg2.OperationalError) could not connect to server: Connection refused
E       	Is the server running on host "localhost" (127.0.0.1) and accepting
E       	TCP/IP connections on port 5432?
E       could not connect to server: Connection refused
E       	Is the server running on host "localhost" (::1) and accepting
E       	TCP/IP connections on port 5432?
E       
E       (Background on this error at: http://sqlalche.me/e/14/e3q8)
```

Therefore, it's important to ensure you're server is running before executing the tests.<br />
