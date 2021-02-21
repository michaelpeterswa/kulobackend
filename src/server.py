from flask import Flask, request, jsonify
from flask_cors import CORS
from tensorflow import keras
import numpy as np
import math

model = keras.models.load_model('../kulo_model')
app = Flask(__name__)
CORS(app)

# https://www.raspberrypi.org/forums/viewtopic.php?t=149371#p982264
def valmap(value, istart, istop, ostart, ostop):
  return ostart + (ostop - ostart) * ((value - istart) / (istop - istart))

def predict(epochx, latx, longx):
    tscl = (5040000.0, 1612339200.0, 0, 1)
    ltscl = (45.556224, 49.00112, 0, 1)
    lnscl = (-124.716371, -116.94347, 0, 1)

    epochx = valmap(epochx, tscl[0], tscl[1], tscl[2], tscl[3])
    latx = valmap(latx, ltscl[0], ltscl[1], ltscl[2], ltscl[3])
    longx = valmap(longx, lnscl[0], lnscl[1], lnscl[2], lnscl[3])

    inp = np.array([(epochx, latx, longx)])
    return model.predict(inp)

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
    epoch_req = float(request.args.get('epoch'))
    lat_req = float(request.args.get('lat'))
    long_req = float(request.args.get('long'))

    ascl = (0.0, 250280.45, 0, 1)

    prediction = predict(epoch_req, lat_req, long_req)
    acres = valmap(prediction[0][0], ascl[2], ascl[3], ascl[0], ascl[1])
    result = {
        "epoch": epoch_req,
        "lat": lat_req,
        "long": long_req,
        "acres": acres,
        "radius": acres_to_circle_radius_in_miles(acres) 
    }
    return jsonify(result)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888)