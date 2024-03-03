from flask import Flask, render_template, request
#from flask_sqlalchemy import SQLAlchemy
#pip3 install boto3 flask
import boto3
#pip install pymysql
import pymysql
from flask import Flask, render_template, request, redirect, url_for, flash
from flask import Flask, render_template

application = Flask(__name__, template_folder="app/HTML")
application.secret_key = 'ben'

# Database connection details
DB_HOST = 'database-1.cjc0q8gai3nl.us-east-2.rds.amazonaws.com'
DB_USER = 'admin'
DB_PASSWORD = 'password'
DB_NAME = 'flask_login'

#for bucket access
AWS_ACCESS_KEY_ID = 'AKIAZI2LHWQSB2BAXAKG'
AWS_SECRET_ACCESS_KEY = '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'
BUCKET_NAME = '422p1bucket'
EXPIRATION_TIME = 3600
s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

# Function to get DB connection
def get_db_connection():
    return pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db=DB_NAME, cursorclass=pymysql.cursors.DictCursor)


@application.route("/", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM users WHERE username = %s AND password = %s"
                cursor.execute(sql, (username, password))
                result = cursor.fetchone()
                if result:
                    flash('Login successful!')
                    return redirect(url_for('home'))
                else:
                    flash('Login Unsuccessful. Please check username and password')
        finally:
            connection.close()

    return render_template('login.html')

@application.route("/new_account", methods=['GET', 'POST'])
def new_account():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO users (username, password) VALUES (%s, %s)"
                cursor.execute(sql, (username, password))
            connection.commit()
            flash('Account created successfully! Please login.')
            return redirect(url_for('login'))
        except pymysql.err.IntegrityError:
            flash('Username already exists. Please choose another one.')
        finally:
            connection.close()
    return render_template('new_account.html')

@application.route("/home", methods=['POST', 'GET'])
def home():   
    try:
        print("TRY")
        response = s3.list_objects_v2(Bucket=BUCKET_NAME)
        objects = response.get('Contents', [])[:10]

        images = []
        for obj in objects:
            
            image_url = f'https://{BUCKET_NAME}.s3.amazonaws.com/{obj["Key"]}'
            # image_url = s3.generate_presigned_url('get_object', Params={'Bucket': BUCKET_NAME, 'Key': obj['Key']}, ExpiresIn=EXPIRATION_TIME)
            caption = obj['Key']  # You may need to modify this depending on how your images are named
            images.append({'url': image_url, 'caption': caption})
    except Exception as e:
        return render_template('home.html')
        return f"Error: {str(e)}", 500
    return  render_template('home.html', images=images)


if __name__ == '__main__':
    application.run(host='0.0.0.0', port='8080', debug=True)
