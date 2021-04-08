from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
	return 'Hello World!'

app.route('/itemDetails')
def item_details():
	return 'ITEM DETAILS'
