from flask import Flask, render_template, request, url_for
from flask_pymongo import PyMongo
import cv2
import gridfs
import numpy as np
from dotenv import load_dotenv
import os

load_dotenv()


app = Flask(__name__)
app.config['MONGO_URI'] = os.getenv('MONGO_URI')
mongo = PyMongo(app)
db_collection = mongo.db.ImageCollection
fs = gridfs.GridFS(mongo.db)


@app.route('/')
def upload_image():
    return render_template('index.html')


@app.route('/upload', methods=['GET', 'POST'])
def create():
    result = False
    username = None
    if request.method == 'POST':
        image = request.files['img']
        username = request.form.get('username')
        phone_number = request.form.get('phone_number')
        if db_collection.find_one({'username': username}):
            return 'Image was upload'
        image_string = image.read()
        img = cv2.imdecode(np.fromstring(image_string, np.uint8), cv2.IMREAD_COLOR)
        image_id = fs.put(img.tostring(), encoding='utf-8')
        mongo.save_file(image.filename, image)
        meta = {
            'username': username,
            'profile_image_name': image.filename,
            'phone_number': phone_number,
            'images': [
                {
                    'imageID': image_id,
                    'shape': img.shape,
                    'dtype': str(img.dtype)
                }
            ]
        }
        result = db_collection.insert_one(meta)
    if result:
        return f'''
            <h1>Done!</h1>
            <a href="/">Add another image</a>
            <a href="/profile/{username}">Watch you image upload</a>
        '''
    else:
        return 'Unsuccessful upload image'


@app.route('/file/<filename>')
def get_image(filename):
    return mongo.send_file(filename)


@app.route('/profile/<username>')
def profile(username):
    user = db_collection.find_one_or_404({'username': username})
    return f'''
            <a href="/">Add another image</a>
            <h1>{username}</h1>
            <img src="{url_for('get_image', filename=user['profile_image_name'])}">
        '''


if __name__ == '__main__':
    app.run()
