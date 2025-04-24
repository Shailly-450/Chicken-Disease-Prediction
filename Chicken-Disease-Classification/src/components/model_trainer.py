import numpy as np
import pandas as pd
import os
import cv2
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten
from src.utils.logger import get_logger

logger = get_logger(__name__)

class ModelTrainer:
    def __init__(self):
        # Define the model with 4 output classes to match the dataset
        self.model = Sequential([
            Flatten(input_shape=(64, 64, 3)),
            Dense(128, activation="relu"),
            Dense(64, activation="relu"),
            Dense(4, activation="softmax")  # Changed from 5 to 4 classes
        ])
        # Label mapping for the 4 classes
        self.label_map = {
            'Salmonella': 0,
            'Coccidiosis': 1,
            'New Castle Disease': 2,
            'Healthy': 3
        }

    def compile_model(self):
        logger.info("Compiling model...")
        self.model.compile(
            optimizer="adam",
            loss="sparse_categorical_crossentropy",
            metrics=["accuracy"]
        )

    def load_dataset(self, csv_path, img_dir, test_size=0.2):
        """
        Load and preprocess the dataset from CSV and image directory.
        
        Args:
            csv_path (str): Path to the train_data.csv file
            img_dir (str): Path to the directory containing images
            test_size (float): Fraction of data to use for validation
        
        Returns:
            X_train, y_train, X_val, y_val: NumPy arrays for training and validation
        """
        logger.info("Loading dataset...")
        
        # Read CSV file
        df = pd.read_csv(csv_path)
        df.columns = ['filepaths', 'labels']
        
        # Update filepaths to full paths
        df['filepaths'] = df['filepaths'].apply(lambda x: os.path.join(img_dir, x))
        
        # Verify all files exist
        df = df[df['filepaths'].apply(os.path.exists)]
        if len(df) == 0:
            raise ValueError("No valid image files found in the specified directory.")
        
        # Map labels to integers
        df['labels'] = df['labels'].map(self.label_map)
        if df['labels'].isna().any():
            raise ValueError("Some labels in the dataset are not in the expected classes.")
        
        # Initialize arrays
        images = []
        labels = []
        
        # Load and preprocess images
        for filepath, label in zip(df['filepaths'], df['labels']):
            # Read image using OpenCV
            img = cv2.imread(filepath)
            if img is None:
                logger.warning(f"Failed to load image: {filepath}")
                continue
            # Convert BGR to RGB
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            # Resize to 64x64
            img = cv2.resize(img, (64, 64))
            # Normalize to [0, 1]
            img = img / 255.0
            images.append(img)
            labels.append(label)
        
        # Convert to NumPy arrays
        X = np.array(images)
        y = np.array(labels)
        
        # Split into training and validation sets
        X_train, X_val, y_train, y_val = train_test_split(
            X, y, test_size=test_size, random_state=42, stratify=y
        )
        
        logger.info(f"Loaded {len(X_train)} training samples and {len(X_val)} validation samples.")
        return X_train, y_train, X_val, y_val

    def train(self, X_train, y_train, X_val, y_val, epochs=10, batch_size=32):
        logger.info("Starting training...")
        history = self.model.fit(
            X_train, y_train,
            validation_data=(X_val, y_val),
            epochs=epochs,
            batch_size=batch_size
        )
        logger.info("Training complete!")
        return history

    def save_model(self, h5_path="src/models/chicken_disease_model.h5", pickle_path=None):
        # Save model in HDF5 format
        self.model.save(h5_path)
        logger.info(f"Model saved at {h5_path}")
        print("✅ Model saved successfully!")
        
        # Optionally save as pickle
        if pickle_path:
            import pickle
            with open(pickle_path, 'wb') as file:
                pickle.dump(self.model, file)
            logger.info(f"Model saved as pickle at {pickle_path}")
            print("✅ Model saved as pickle successfully!")

if __name__ == "__main__":
    # Paths to dataset
    csv_path = "Chicken-Disease-Classification/data/train_data.csv"
    img_dir = "Chicken-Disease-Classification/data/Train"
    
    # Initialize trainer
    trainer = ModelTrainer()
    trainer.compile_model()
    
    # Load dataset
    X_train, y_train, X_val, y_val = trainer.load_dataset(csv_path, img_dir, test_size=0.2)
    
    # Train model
    trainer.train(X_train, y_train, X_val, y_val, epochs=10, batch_size=32)
    
    # Save model
    trainer.save_model(
        h5_path="Chicken-Disease-Classification/src/models/my_model.h5",
        pickle_path="Chicken-Disease-Classification/src/models/my_model.pkl"
    )