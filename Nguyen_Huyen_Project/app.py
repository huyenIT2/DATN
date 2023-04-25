from flask import Flask, jsonify, request
import json
from flask_cors import CORS, cross_origin
from main import HelloFace
import numpy as np
from PIL import Image

model = HelloFace()

app = Flask(__name__)

# Apply Flask CORS
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/predict', methods = ['GET', 'POST'])
@cross_origin(origin='*')
def predict():
    global res
    
    if(request.method == "POST"):
        img = request.files['image']
        img = np.array(Image.open(img)).astype('uint8')
        res = model.process_frame(img)
        return jsonify({'msv':res})
        

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port='6868')