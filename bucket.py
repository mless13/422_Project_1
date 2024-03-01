#pip3 install boto3 flask

import boto3
from flask import Flask, render_template

#initialization 
app = Flask(__name__)
AWS_ACCESS_KEY_ID = 'your_access_key_id'
AWS_SECRET_ACCESS_KEY = 'your_secret_access_key'
BUCKET_NAME = '422p1bucket'
s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

@app.route('/')
def bucket():
    response = s3.list_objects_v2(Bucket=BUCKET_NAME)

    #get 10 images
    objects = response['Contents'][:10]

    # Extract URLs and captions
    images = []
    for obj in objects:
        image_url = s3.generate_presigned_url('get_object', Params={'Bucket': BUCKET_NAME, 'Key': obj['Key']})
        caption = obj['Key']  # You may need to modify this depending on how your images are named
        images.append({'url': image_url, 'caption': caption})

    # Render HTML template with images and captions
    return render_template('./HTML/home.html', images=images)

if __name__ == '__main__':
    app.run(debug=True)


