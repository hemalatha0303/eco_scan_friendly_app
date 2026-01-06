import os
import io
import numpy as np
import cv2
import tensorflow as tf
from flask import Flask, request, jsonify
from flask_cors import CORS
from ultralytics import YOLO
from PIL import Image

# ---------------------------------------------------------
# FLASK APP
# ---------------------------------------------------------
app = Flask(__name__)
CORS(app)

# ---------------------------------------------------------
# GLOBAL MODELS (LAZY LOAD)
# ---------------------------------------------------------
veg_model = None
soil_model = None

VEG_MODEL_PATH = "models/vegetation_model.h5"
SOIL_MODEL_PATH = "models/best.pt"

# ---------------------------------------------------------
# MODEL LOADERS
# ---------------------------------------------------------
def load_veg_model():
    global veg_model
    if veg_model is None:
        print("Loading vegetation model...")
        veg_model = tf.keras.models.load_model(VEG_MODEL_PATH)
    return veg_model

def load_soil_model():
    global soil_model
    if soil_model is None:
        print("Loading soil model...")
        soil_model = YOLO(SOIL_MODEL_PATH)
    return soil_model

# ---------------------------------------------------------
# PREPROCESSING
# ---------------------------------------------------------
def preprocess_veg(img_bytes, target_size=(256, 256), normalize_type="0_1"):
    """
    Preprocess vegetation image for model prediction.
    normalize_type: "0_1" -> scale 0-1
                    "-1_1" -> scale -1 to 1
    """
    # Load image and convert to RGB
    img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
    img = np.array(img)

    # Resize
    img = cv2.resize(img, target_size, interpolation=cv2.INTER_AREA)

    # Float32
    img = img.astype(np.float32)

    # Normalize
    if normalize_type == "0_1":
        img /= 255.0
    elif normalize_type == "-1_1":
        img = (img / 127.5) - 1.0

    # Add batch dimension
    return np.expand_dims(img, axis=0)

# ---------------------------------------------------------
# ROUTES
# ---------------------------------------------------------
@app.route("/")
def home():
    return "EcoScan AI Backend Running"

# ---- WARMUP MODELS ----
@app.route("/warmup")
def warmup():
    load_veg_model()
    load_soil_model()
    return "Models loaded"

# ---- VEGETATION PREDICTION ----
@app.route("/predict/vegetation", methods=["POST"])
def predict_vegetation():
    try:
        if "file" not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        model = load_veg_model()
        img_bytes = request.files["file"].read()
        input_tensor = preprocess_veg(img_bytes)

        # Predict
        prediction = model.predict(input_tensor, verbose=0)

        # Remove batch/channel dimensions
        if prediction.ndim == 4:
            prediction = np.squeeze(prediction, axis=0)
            if prediction.shape[-1] == 1:
                prediction = np.squeeze(prediction, axis=-1)

        # Clip and threshold
        prediction = np.clip(prediction, 0, 1)
        mask = (prediction >= 0.5).astype(np.uint8)

        # Coverage calculation
        coverage = (np.sum(mask) / mask.size) * 100

        return jsonify({
            "status": "success",
            "coverage": round(float(coverage), 2)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ---- SOIL PREDICTION ----
@app.route("/predict/soil", methods=["POST"])
def predict_soil():
    try:
        if "file" not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        model = load_soil_model()
        img_bytes = request.files["file"].read()
        img = Image.open(io.BytesIO(img_bytes))

        # YOLO prediction
        results = model(img)[0]

        if len(results.boxes) == 0:
            return jsonify({
                "status": "not_detected",
                "label": "Unknown",
                "confidence": 0
            })

        box = results.boxes[0]
        class_id = int(box.cls[0])
        label = model.names[class_id]
        confidence = float(box.conf[0])

        return jsonify({
            "status": "success",
            "label": label,
            "confidence": round(confidence, 4)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ---------------------------------------------------------
# MAIN
# ---------------------------------------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
