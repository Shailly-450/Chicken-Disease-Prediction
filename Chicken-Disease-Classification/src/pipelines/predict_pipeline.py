import tensorflow as tf
import numpy as np
import cv2
from src.utils.logger import get_logger

logger = get_logger(__name__)

class PredictPipeline:
    def __init__(self, model_path="src/models/my_model.h5"):
        """
        Initialize the prediction pipeline by loading the model.

        Args:
            model_path (str): Path to the trained model file (.h5).
        
        Raises:
            FileNotFoundError: If the model file does not exist.
            Exception: If model loading fails.
        """
        try:
            if not tf.io.gfile.exists(model_path):
                raise FileNotFoundError(f"Model file not found at: {model_path}")
            self.model = tf.keras.models.load_model(model_path)
            logger.info(f"Model loaded successfully from {model_path}")
        except Exception as e:
            logger.error(f"Failed to load model: {str(e)}")
            raise
        
        # Define label map consistent with ModelTrainer
        self.label_map = {
            0: 'Salmonella',
            1: 'Coccidiosis',
            2: 'New Castle Disease',
            3: 'Healthy'
        }

    def predict(self, img_path):
        """
        Predict the disease class for an input image.

        Args:
            img_path (str): Path to the input image file.

        Returns:
            dict: Dictionary containing probabilities and predicted class name.

        Raises:
            FileNotFoundError: If the image file does not exist.
            ValueError: If the image cannot be loaded or processed.
        """
        logger.info(f"Predicting for {img_path}...")
        
        # Validate image path
        if not tf.io.gfile.exists(img_path):
            logger.error(f"Image file not found: {img_path}")
            raise FileNotFoundError(f"Image file not found: {img_path}")

        # Load and preprocess image using OpenCV for consistency with ModelTrainer
        try:
            img = cv2.imread(img_path)
            if img is None:
                raise ValueError(f"Failed to load image: {img_path}")
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = cv2.resize(img, (64, 64))
            img_array = img / 255.0
            img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
        except Exception as e:
            logger.error(f"Image processing failed: {str(e)}")
            raise ValueError(f"Failed to process image: {str(e)}")

        # Predict
        try:
            probabilities = self.model.predict(img_array, verbose=0)[0]
            predicted_class_idx = np.argmax(probabilities)
            predicted_class = self.label_map[predicted_class_idx]
            logger.info(f"Prediction: {predicted_class} (Probabilities: {probabilities.tolist()})")
            return {
                "probabilities": probabilities.tolist(),
                "predicted_class": predicted_class
            }
        except Exception as e:
            logger.error(f"Prediction failed: {str(e)}")
            raise ValueError(f"Prediction failed: {str(e)}")