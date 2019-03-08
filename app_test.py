from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/login')
def log_in():
	user_info = { 'user':'demo', 'pass':'demo' } 
	return 'Login page!'

@app.route('/validate_identity')
def validate_identity():
	return 'Identity page!'
