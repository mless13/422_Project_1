from flask import Flask, render_template, request
#from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder="app/HTML")

@app.route("/")
def login():
    return  render_template('login.html')

@app.route("/new_account")
def new_login():
    return render_template('new_account.html')

@app.route("/home", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

    return  render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)