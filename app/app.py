from flask import Flask, request, Response 
import jsonpickle
from flask_uploads import UploadSet, IMAGES, configure_uploads
import cv2
import numpy as np
import cvlib as cv
from PIL import Image
import subprocess

app = Flask(__name__)


# Configure the app to store uploaded files in the 'uploads' folder
app.config['UPLOADS_DEFAULT_DEST'] = 'vol1'

# Create an UploadSet for handling image uploads
images = UploadSet('images', IMAGES)

# Configure the Flask-Uploads extension
configure_uploads(app, (images,))

filename = ''


@app.route('/api/test', methods=['GET'])
def test():
    # Model code
    response = {'message': 'API hit iimv'}
    # encode response using jsonpickle
    response_pickled = jsonpickle.encode(response)

    return Response(response=response_pickled, status=200, mimetype="application/json")


@app.route('/api/upload', methods=['POST'])
def upload():
    # Check if a file was uploaded
    if 'image' not in request.files:
        return 'No file uploaded', 400

    # Save the uploaded file
    filename = images.save(request.files['image'])
    img = Image.open(filename)
    img = np.array(img)

    results = cv.detect_common_objects(img, model='yolov3')
    my_string = str(results)

    # Return the filename of the saved file
    return my_string, 200


@app.route('/api/detect', methods=['GET'])
def detect():

    img = Image.open('vol1/images/car.jpg')
    img = np.array(img)

    results = cv.detect_common_objects(img, model='yolov3')
    my_string = str(results)

    # Return the filename of the saved file
    return my_string, 200


@app.route('/api/detect2', methods=['GET'])
def detect_two():
    # Run the 'ls' command to list the files in the current directory
    result = subprocess.run(['python yolo_opencv.py --image vol1/images/car.jpg --config yolov3.cfg --weights yolov3.weights --classes yolov3.txt'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Print the output of the command
    print(result.stdout.decode('utf-8'))
  
    return result.stdout.decode('utf-8'), 200






if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)