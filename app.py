from flask import Flask, render_template, request
#from flask_sqlalchemy import SQLAlchemy

application = Flask(__name__, template_folder="app/HTML")

@application.route("/")
def login():
    return  render_template('login.html')

@application.route("/new_account")
def new_login():
    return render_template('new_account.html')

@application.route("/home", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

    return  render_template('home.html')

if __name__ == '__main__':
    application.run(host='0.0.0.0', port='8080', debug=True)
