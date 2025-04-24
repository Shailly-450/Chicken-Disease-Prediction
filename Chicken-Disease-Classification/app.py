import os
from flask import Flask, request, jsonify
from PIL import Image
from src.pipelines.predict_pipeline import PredictPipeline
from flask_cors import CORS
from src.utils.logger import get_logger

# Initialize Flask app and logger
app = Flask(__name__)
logger = get_logger(__name__)
app.logger.handlers = logger.handlers
app.logger.setLevel(logger.level)

# Configure CORS (restrict in production)
CORS(app)  # For development; in production, specify origins

# Initialize predictor
try:
    predictor = PredictPipeline(model_path="src/models/chicken_disease_model.h5")
except Exception as e:
    logger.error(f"Failed to initialize PredictPipeline: {str(e)}")
    raise

# Ensure temp directory exists
os.makedirs("temp", exist_ok=True)

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Chicken Disease Classification API Running!"})

@app.route("/health", methods=["GET"])
def health():
    try:
        if predictor and predictor.model:
            return jsonify({"status": "healthy", "model": "loaded"}), 200
        return jsonify({"status": "error", "model": "not loaded"}), 500
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/predict", methods=["POST"])
def predict():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files["file"]
    
    # Validate file extension
    allowed_extensions = {'.jpg', '.jpeg', '.png'}
    if not os.path.splitext(file.filename)[1].lower() in allowed_extensions:
        return jsonify({"error": "Invalid file extension. Only .jpg, .jpeg, .png allowed."}), 400

    # Check file size (limit to 5MB)
    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    if file_size > 5 * 1024 * 1024:
        return jsonify({"error": "File size exceeds 5MB limit."}), 400
    file.seek(0)

    # Verify image
    try:
        img = Image.open(file)
        img.verify()
        file.seek(0)
    except Exception as e:
        return jsonify({"error": f"Invalid image file: {str(e)}"}), 400

    # Save file
    file_path = f"temp/{file.filename}"
    file.save(file_path)
    app.logger.info(f"File saved at: {file_path}")

    # Run prediction
    try:
        prediction = predictor.predict(file_path)
        app.logger.info(f"Prediction result: {prediction}")
        return jsonify({"prediction": prediction})
    except Exception as e:
        return jsonify({"error": f"Failed to process image: {str(e)}"}), 500
    finally:
        # Clean up temp file
        if os.path.exists(file_path):
            os.remove(file_path)
            app.logger.info(f"File deleted: {file_path}")

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=8000)