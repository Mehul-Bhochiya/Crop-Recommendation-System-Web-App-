from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import pickle

# Load model
with open("model.pkl", "rb") as f:
    data = pickle.load(f)
    model = data["model"]
    sc = data["standard_scaler"]
    ms = data["minmax_scaler"]

# Flask setup
app = Flask(__name__)
CORS(app)  # This allows mobile app to connect

# Crop mapping
crop_dict = {
    "rice": "Rice", "maize": "Maize", "jute": "Jute", "cotton": "Cotton", "coconut": "Coconut",
    "papaya": "Papaya", "orange": "Orange", "apple": "Apple", "muskmelon": "Muskmelon",
    "watermelon": "Watermelon", "grapes": "Grapes", "mango": "Mango", "banana": "Banana",
    "pomegranate": "Pomegranate", "lentil": "Lentil", "blackgram": "Blackgram", "mungbean": "Mungbean",
    "mothbeans": "Mothbeans", "pigeonpeas": "Pigeonpeas", "kidneybeans": "Kidneybeans",
    "chickpea": "Chickpea", "coffee": "Coffee"
}

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.json
        print("Incoming Data:", data)  # Add this line

        features = np.array([[data["N"], data["P"], data["K"], data["temp"], data["humidity"], data["ph"], data["rainfall"]]])
        scaled = sc.transform(features)
        final = ms.transform(scaled)
        prediction = model.predict(final)[0]
        result = crop_dict.get(prediction, "Unknown Crop")
        return jsonify({"crop": result})
    except Exception as e:
        print("Error:", e)  # Add this line
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)

