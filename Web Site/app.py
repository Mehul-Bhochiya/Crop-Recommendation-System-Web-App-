import numpy as np
from flask import Flask, render_template, request
import pickle

# Load model and scalers from one file
try:
    with open('model.pkl', 'rb') as f:
        data = pickle.load(f)
        model = data['model']
        sc = data['standard_scaler']
        ms = data['minmax_scaler']
except FileNotFoundError as e:
    print(f"Error: {e}")
    exit(1)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/crop/<crop_name>')
def crop_page(crop_name):
    try:
        return render_template(f"crops/{crop_name}.html")
    except:
        return "Crop page not found", 404

@app.route("/predict", methods=['POST'])
def predict():
    try:
        N = float(request.form['Nitrogen'])
        P = float(request.form['Phosporus'])
        K = float(request.form['Potassium'])
        temp = float(request.form['Temperature'])
        humidity = float(request.form['Humidity'])
        ph = float(request.form['Ph'])
        rainfall = float(request.form['Rainfall'])

        feature_list = np.array([[N, P, K, temp, humidity, ph, rainfall]])
        scaled_features = sc.transform(feature_list)
        final_features = ms.transform(scaled_features)

        prediction = model.predict(final_features)

        crop_dict = {
            "rice": "Rice", "maize": "Maize", "jute": "Jute", "cotton": "Cotton", "coconut": "Coconut",
            "papaya": "Papaya", "orange": "Orange", "apple": "Apple", "muskmelon": "Muskmelon",
            "watermelon": "Watermelon", "grapes": "Grapes", "mango": "Mango", "banana": "Banana",
            "pomegranate": "Pomegranate", "lentil": "Lentil", "blackgram": "Blackgram", "mungbean": "Mungbean",
            "mothbeans": "Mothbeans", "pigeonpeas": "Pigeonpeas", "kidneybeans": "Kidneybeans",
            "chickpea": "Chickpea", "coffee": "Coffee"
        }

        predicted_crop = prediction[0]
        if predicted_crop in crop_dict:
            crop = crop_dict[predicted_crop]
            result = f"{crop} is the best crop to be cultivated right there."
        else:
            result = "Sorry, we could not determine the best crop to be cultivated."

        return render_template("index.html", result=result)

    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    app.run(debug=True)
