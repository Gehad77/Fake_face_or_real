from flask import Flask, request, render_template, jsonify
import numpy as np
import tensorflow as tf
import os
from PIL import Image

model = tf.keras.models.load_model('model.h5')
app = Flask(__name__, template_folder='template')

@app.route("/", methods=['GET'])
def hello():
    return render_template("index.html")


@app.route("/", methods=['POST'])
def predict():
    # Save the uploaded image
    imagefile = request.files['imagefile']
    directory = './real_vs_fake/'
    if not os.path.exists(directory):
        os.makedirs(directory)
    image_path = os.path.join(directory, imagefile.filename)
    imagefile.save(image_path)

    # Open the image
    img = Image.open(image_path)
    resized_img = img.resize((128, 128))
    img_array = np.array(resized_img) / 255.0

    # Make a prediction using the model
    prediction = model.predict(np.expand_dims(img_array, axis=0))
    prediction_value = prediction[0][0]

    # Check if the image is real or fake 
    if prediction_value >= 0.5:
        message = 'The image is real.'
    else:
        message = 'The image is fake.'

    # Return the prediction message as a valid response
    return message

    # Return the prediction and message as a JSON response
    return jsonify({'prediction': float(prediction), 'message': message})

if __name__ =='__main__':
    app.run(port=8080, debug=True)
