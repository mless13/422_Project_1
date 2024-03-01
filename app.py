from flask import Flask, render_template, request
#from flask_sqlalchemy import SQLAlchemy
#pip3 install boto3 flask
import boto3


application = Flask(__name__, template_folder="app/HTML")

#for bucket access
AWS_ACCESS_KEY_ID = 'AKIAZI2LHWQSKEKULJUU'
AWS_SECRET_ACCESS_KEY = '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'
BUCKET_NAME = '422p1bucket'
s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

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
        
    try:

If your images are named in the format burger.jpg, cake.jpg, etc., and you want to use the image filenames as the alt attributes, you can directly use the image filenames without any modification. Here's how you can adjust the code:

python
Copy code
from flask import Flask, render_template
import boto3

app = Flask(__name__)

# AWS S3 credentials
AWS_ACCESS_KEY_ID = 'your_access_key_id'
AWS_SECRET_ACCESS_KEY = 'your_secret_access_key'
BUCKET_NAME = 'your_bucket_name'

# Initialize Boto3 S3 client
s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

@app.route("/home")
def home():
    try:
        response = s3.list_objects_v2(Bucket=BUCKET_NAME)
        objects = response.get('Contents', [])[:10]

        images = []
        for obj in objects:
            image_url = s3.generate_presigned_url('get_object', Params={'Bucket': BUCKET_NAME, 'Key': obj['Key']})
            image_name = obj['Key'].split('/')[-1]  # Extract filename from the object key
            images.append({'url': image_url, 'alt': image_name})
    except Exception as e:
      
        return f"Error: {str(e)}", 500

    return  render_template('home.html', images=images)


if __name__ == '__main__':
    application.run(host='0.0.0.0', port='8080', debug=True)
