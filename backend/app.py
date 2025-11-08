import os
from datetime import datetime
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import tensorflow as tf
import numpy as np
from PIL import Image
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# ✅ ✅ Save uploaded images in this folder
UPLOAD_DIR = r"C:\\Users\\harsh\\OneDrive\\Desktop\\Deep Learning\\PlantVillage"
os.makedirs(UPLOAD_DIR, exist_ok=True)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_DIR = os.path.join(BASE_DIR, "model")
MODEL_H5 = os.path.join(BASE_DIR, "model.h5")
MODEL_KERAS = os.path.join(BASE_DIR, "model.keras")

model = None

# ✅ Try loading .keras
if os.path.isfile(MODEL_KERAS):
    print("✅ Loading model.keras")
    model = tf.keras.models.load_model(MODEL_KERAS)

# ✅ Try loading .h5
elif os.path.isfile(MODEL_H5):
    print("✅ Loading model.h5")
    model = tf.keras.models.load_model(MODEL_H5)

# ✅ Try SavedModel folder
elif os.path.isdir(MODEL_DIR) and os.path.exists(os.path.join(MODEL_DIR, "saved_model.pb")):
    print("✅ Loading SavedModel with TFSMLayer")
    model = tf.keras.layers.TFSMLayer(MODEL_DIR, call_endpoint="serving_default")

else:
    raise FileNotFoundError("❌ No model found. Put model.h5, model.keras, or SavedModel inside backend folder")

# ✅ Detect input size
try:
    if hasattr(model, "input_shape"):
        IMG_SIZE = int(model.input_shape[1])
    else:
        IMG_SIZE = 224
except:
    IMG_SIZE = 224

# ✅ Class names from .env
CLASS_NAMES = os.getenv("CLASS_NAMES", "Potato___Early_blight,Potato___Late_blight,Tomato_healthy").split(",")
CLASS_NAMES = [c.strip() for c in CLASS_NAMES if c.strip()]

# ✅ MongoDB Setup
MONGO_URI = os.getenv("MONGO_URI", "")
history_col = None

if MONGO_URI:
    try:
        client = MongoClient(MONGO_URI)
        db = client[os.getenv("MONGO_DB", "airy_ai_db")]
        history_col = db[os.getenv("MONGO_COLLECTION", "history")]
        print("✅ MongoDB Connected")
    except Exception as e:
        print("❌ MongoDB error:", e)
else:
    print("⚠ No MONGO_URI in .env — History disabled")

# ✅ Preprocessing
def preprocess_img(path):
    img = Image.open(path)
    if img.mode != "RGB":
        img = img.convert("RGB")
    img = img.resize((IMG_SIZE, IMG_SIZE))
    arr = np.array(img) / 255.0
    arr = np.expand_dims(arr, axis=0)
    return arr

# ✅ Prediction API
@app.route("/predict", methods=["POST"])
def predict():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files["image"]
    save_path = os.path.join(UPLOAD_DIR, file.filename)
    file.save(save_path)

    img = preprocess_img(save_path)

    if isinstance(model, tf.keras.layers.TFSMLayer):
        outputs = model(img)
        preds = outputs[list(outputs.keys())[0]].numpy()[0]
    else:
        preds = model.predict(img)[0]

    idx = int(np.argmax(preds))
    label = CLASS_NAMES[idx]
    confidence = float(preds[idx])

    record = {
        "image": save_path,
        "label": label,
        "confidence": confidence,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    if history_col:
        history_col.insert_one(record.copy())

    # remove local path from response
    record["image"] = f"/uploads/{file.filename}"

    return jsonify(record)

# ✅ Serve uploaded images
@app.route("/uploads/<path:filename>")
def serve_upload(filename):
    return send_from_directory(UPLOAD_DIR, filename)

# ✅ Show History
@app.route("/history", methods=["GET"])
def history():
    if not history_col:
        return jsonify({"error": "MongoDB not configured"}), 500

    data = []
    for x in history_col.find().sort("_id", -1).limit(20):
        x["_id"] = str(x["_id"])
        data.append(x)
    return jsonify(data)

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "OK", "img_size": IMG_SIZE, "classes": CLASS_NAMES})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
