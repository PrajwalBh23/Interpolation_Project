from flask import Flask, request, jsonify
import pandas as pd
from scipy.interpolate import griddata
from flask_cors import CORS
import numpy as np

app = Flask(__name__)
CORS(app)

# Read data from Excel
df = pd.read_excel('Interpolation.xlsx', engine='openpyxl')

# Convert DataFrame to list of dictionaries
districts = df.to_dict(orient='records')

def interpolate_temperature(lat, lon):
    coords = df[['Latitude', 'Longitude']].values
    temps = df['Temperature'].values

    temp = griddata(coords, temps, (lat, lon), method='linear')
    return temp

@app.route('/data', methods=['GET'])
def get_data():
    return jsonify(districts)

@app.route('/interpolate', methods=['GET'])
def interpolate():
    lat = float(request.args.get('lat'))
    lon = float(request.args.get('lon'))
    temp = interpolate_temperature(lat, lon)

    if temp is None or np.isnan(temp):
        return jsonify({"error": "Interpolation failed. Coordinates might be out of the range."}), 400

    return jsonify({"temp": temp.item()})

if __name__ == '__main__':
    app.run(debug=True)
