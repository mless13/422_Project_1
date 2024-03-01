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
        response = s3.list_objects_v2(Bucket=BUCKET_NAME)
        objects = response.get('Contents', [])[:10]

        images = []
        for obj in objects:
            image_url = s3.generate_presigned_url('get_object', Params={'Bucket': BUCKET_NAME, 'Key': obj['Key']})
            caption = obj['Key']  # You may need to modify this depending on how your images are named
            images.append({'url': image_url, 'caption': caption})
    except Exception as e:
      
        return f"Error: {str(e)}", 500

    return  render_template('home.html', images=images)


if __name__ == '__main__':
    application.run(host='0.0.0.0', port='8080', debug=True)
