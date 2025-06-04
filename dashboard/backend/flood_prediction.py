"""Flood Prediction Model Service using Tensorflow"""

from pathlib import Path
from threading import Lock
import tensorflow as tf
import reflex as rx
from typing import Optional, List



class FloodPredictionModel:
    """Singleton model class that loads TensorFlow model only once."""

    _instance: Optional["FloodPredictionModel"] = None
    _lock: Lock = Lock()

    def __init__(self):
        """Private constructor - use get_instance() instead."""
        self._model: Optional[tf.keras.Model] = None
        self._model_path: Optional[str] = None
        self._is_loaded: bool = False
        self.batch_size: int = 32
        self.sigmoid_threshold: float = 0.5

    @classmethod
    def get_instance(cls) -> "FloodPredictionModel":
        """Get singleton instance using double-checked locking."""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls()
        return cls._instance

    def set_batch_size(self, batch_size: int) -> None:
        """Set batch size for model predictions."""
        if batch_size <= 0:
            raise ValueError("Batch size must be a positive integer")
        self.batch_size = batch_size

    @property
    def is_loaded(self) -> bool:
        """Check if model is loaded."""
        return self._is_loaded and self._model is not None

    def load_if_needed(self, model_path: str) -> None:
        """Load model only if not already loaded or path changed."""
        model_path = Path(model_path)

        if not model_path.exists():
            raise FileNotFoundError(f"Model file not found: {model_path}")

        if self._is_loaded and self._model_path == model_path:
            return

        with self._lock:
            if self._is_loaded and self._model_path == model_path:
                return

            self._load_model(model_path)

    def _load_model(self, model_path: str) -> None:
        """Internal method to load the model."""
        print(f"Loading model from {model_path}...")

        try:
            self._model: tf.keras.models = tf.keras.models.load_model(model_path)
            self._model_path = model_path
            self._is_loaded = True

        except Exception as e:
            self._is_loaded = False
            self._model = None
            self._model_path = None
            raise RuntimeError(f"Failed to load model: {e}")
    def preprocess(self, input_data: List[float]) -> tf.Tensor:
        """Preprocess input data for model prediction."""
        if not self.is_loaded:
            raise RuntimeError("Model not loaded")

        # Convert input data to tensor and reshape as needed
        input_tensor = tf.data.Dataset.from_tensor_slices(input_data)
        input_tensor = input_tensor.batch(self.batch_size)
        input_tensor = input_tensor.prefetch(tf.data.AUTOTUNE)
        return input_tensor

    def predict(self, input_data: List[float]) -> float:
        """Make prediction with loaded model."""
        if not self.is_loaded:
            raise RuntimeError("Model not loaded")

        try:
            input_tensor = self.preprocess(input_data)
            prediction = self._model.predict(input_tensor, verbose=0)
            result = self.post_processor(prediction)
            # Return single prediction value
            return result

        except Exception as e:
            raise RuntimeError(f"Prediction failed: {e}")

    def post_processor(self, result: tf.Tensor) -> float:
        """Post-process the prediction result."""
        class_id = tf.cast(tf.greater_equal(result, self.sigmoid_threshold), tf.int32)
        return class_id

    def get_model_info(self) -> dict:
        """Get information about the loaded model."""
        if not self.is_loaded:
            return {"status": "not_loaded"}

        return {
            "status": "loaded",
            "path": self._model_path,
            "input_shape": self._model.input_shape,
            "output_shape": self._model.output_shape,
        }
