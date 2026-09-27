from flask import Flask, request, jsonify
import pandas as pd
import joblib
import os

# Create Flask application
app = Flask(__name__)

# Get project folder path
base_path = os.path.dirname(os.path.abspath(__file__))

# Load trained model
model_path = os.path.join(
    base_path,
    "models",
    "water_quality_model.pkl"
)

# Load label encoder
encoder_path = os.path.join(
    base_path,
    "models",
    "label_encoder.pkl"
)

model = joblib.load(model_path)
label_encoder = joblib.load(encoder_path)

print("Model loaded successfully!")
print("Label encoder loaded successfully!")


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Smart Water Quality Monitoring API is running",
        "status": "OK"
    })


# Prediction API
@app.route("/predict", methods=["POST"])
def predict():

    try:
        # Receive JSON data
        data = request.get_json()

        # Get water parameters
        pH = float(data["pH"])
        TDS_ppm = float(data["TDS_ppm"])
        Turbidity_NTU = float(data["Turbidity_NTU"])
        Temperature_C = float(data["Temperature_C"])

        # Create input DataFrame
        sample = pd.DataFrame({
            "pH": [pH],
            "TDS_ppm": [TDS_ppm],
            "Turbidity_NTU": [Turbidity_NTU],
            "Temperature_C": [Temperature_C]
        })

        # Run the trained model
        model_prediction = model.predict(sample)

        # Convert numerical prediction back to Safe/Unsafe
        model_label = label_encoder.inverse_transform(
            model_prediction
        )[0]

        # Water quality safety rules
        if (
            (6.5 <= pH <= 8.5)
            and (TDS_ppm <= 500.0)
            and (Turbidity_NTU <= 5.0)
            and (5.0 <= Temperature_C <= 30.0)
        ):
            predicted_label = "Safe"
        else:
            predicted_label = "Unsafe"

        # Return result
        return jsonify({
            "prediction": predicted_label
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 400


# Run Flask server
if __name__ == "__main__":
    app.run(debug=True)