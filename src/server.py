from flask import Flask, request, jsonify
from tensorflow import keras
import math

model = keras.models.load_model('../kulo_model')
app = Flask(__name__)

def predict(latitude, longitude):
    lat_amt = 100
    long_amt = 200

    return model.predict([(latitude / lat_amt, longitude / long_amt)])

def acres_to_circle_radius_in_miles(acres):
    sqft = acres * 43560
    radius = math.sqrt(sqft / math.pi)
    return radius / 5280

@app.route('/', methods=['GET'])
def main_route():
    return "kulo backend"

@app.route('/api/predict')
def return_prediction():
    max_acreage = 255900
    lat_req = float(request.args.get('lat'))
    long_req = float(request.args.get('long'))

    prediction = predict(lat_req, long_req)
    acres = prediction[0][0] * max_acreage
    result = {
        "lat": lat_req,
        "long": long_req,
        "acres": acres,
        "radius": acres_to_circle_radius_in_miles(acres) 
    }
    return jsonify(result)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888)