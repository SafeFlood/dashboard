from threading import Lock
import asyncio
import os
import reflex as rx
from typing import Optional, List, Tuple
import pandas as pd
import pickle
from sklearn.preprocessing import StandardScaler
from .flood_prediction import FloodPredictionModel


class DataLoader:
    """Simple singleton data loader."""

    _instance: Optional["DataLoader"] = None
    _lock: Lock = Lock()

    def __init__(self):
        self._data: Optional[pd.DataFrame] = None
        self._scaler: Optional[StandardScaler] = None
        self._is_loaded: bool = False
        self._scaler_loaded: bool = False

    @classmethod
    def get_instance(cls) -> "DataLoader":
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls()
        return cls._instance

    @property
    def is_loaded(self) -> bool:
        return self._is_loaded and self._data is not None

    def load_data(self, data_path: Optional[str] = None) -> None:
        if self._is_loaded:
            return

        if data_path is None:
            data_path = os.path.join(
                os.getcwd(), "dashboard", "data", "flood_inference_data.csv"
            )

        with self._lock:
            if self._is_loaded:
                return

            self._data = pd.read_csv(data_path)
            self._is_loaded = True

    def load_scaler(self, scaler_path: Optional[str] = None) -> None:
        """Load the fitted StandardScaler from pickle file."""
        if self._scaler_loaded:
            return

        if scaler_path is None:
            scaler_path = os.path.join(os.getcwd(), "dashboard", "models", "standard_scaler.pkl")

        with self._lock:
            if self._scaler_loaded:
                return

            try:
                with open(scaler_path, "rb") as f:
                    self._scaler = pickle.load(f)
                self._scaler_loaded = True
                print(f"Scaler loaded from {scaler_path}")
            except Exception as e:
                print(f"Failed to load scaler: {e}")
                self._scaler = None

    def get_data(self) -> pd.DataFrame:
        if not self._is_loaded:
            self.load_data()
        return self._data

    def get_ground_truth(self) -> List[List[float]]:
        """Get ground truth data (lat, lon, target) - not affected by scaler."""
        if not self._is_loaded:
            self.load_data()
        return self._data[["lat", "lon"]].values.tolist()

    def get_coordinates(self) -> List[List[float]]:
        """Get coordinates (lat, lon) - not affected by scaler."""
        if not self._is_loaded:
            self.load_data()
        return self._data[["lat", "lon"]].values.tolist()

    def get_features_scaled(self) -> pd.DataFrame:
        """Get scaled features for model prediction."""
        if not self._is_loaded:
            self.load_data()

        # Get only feature columns (exclude lat, lon, target)
        feature_columns = [
            col for col in self._data.columns if col not in ["target"]
        ]
        features = self._data[feature_columns].copy()

        # Load and apply scaler
        if not self._scaler_loaded:
            self.load_scaler()

        if self._scaler is not None:
            try:
                scaled_features = self._scaler.transform(features)
                return pd.DataFrame(scaled_features, columns=features.columns)
            except Exception as e:
                print(f"Error scaling features: {e}")
                return features

        return features

    def get_features_raw(self) -> pd.DataFrame:
        """Get raw features without scaling."""
        if not self._is_loaded:
            self.load_data()

        feature_columns = [
            col for col in self._data.columns if col not in ["lat", "lon", "target"]
        ]
        return self._data[feature_columns]


def get_ground_truth_targets() -> List[List[float]]:
    """Get ground truth with targets (lat, lon, target) - not affected by scaler."""
    data_loader = DataLoader.get_instance()
    return data_loader.get_ground_truth()


def load_example_inference_data() -> Tuple[List[List[float]], pd.DataFrame]:
    """Load example inference data for testing."""
    data_loader = DataLoader.get_instance()

    ground_truth = data_loader.get_coordinates()

    X = data_loader.get_features_scaled()

    return ground_truth, X


class MapState(rx.State):
    ground_truth_coordinates: list = get_ground_truth_targets()

    predicted_flood_coordinates: list = []

    def clear_coordinates(self) -> None:
        """Clear all coordinates from the map."""
        self.coordinates = []

    @rx.event(background=True)
    async def run_flood_prediction(self) -> float:
        """Run flood prediction using the model."""
        print("Starting flood prediction...")
        try:
            model = FloodPredictionModel.get_instance()
            ground_truth, input_data = load_example_inference_data()
            if not model.is_loaded:
                raise RuntimeError("Flood prediction model is not loaded")
            prediction = model.predict(input_data)
            print(f"Prediction completed: {(len(prediction), prediction[:10])} samples predicted.")
            df = pd.DataFrame({
            'lat': [coord[0] for coord in ground_truth],
            'lon': [coord[1] for coord in ground_truth], 
            'target': prediction
        })
        
        # Filter for flood predictions (target != 0) and get coordinates
            flood_coords = df.query("target != 0")[['lat', 'lon']].values.tolist()
            print(f"Predicted flood coordinates: {flood_coords[:10]} coordinates.")

            async with self:
                self.predicted_flood_coordinates = flood_coords
            print(f"Flood prediction completed: {len(flood_coords)} coordinates predicted.")
        except Exception as e:
            print(f"Error during flood prediction: {e}")
        
    @rx.event
    def set_flood_prediction_coordinates(self):
        """Set the predicted flood coordinates."""
        print("Run flood prediction")
        
        yield MapState.run_flood_prediction

    

