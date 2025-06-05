import numpy as np
from dashboard.backend import FloodPredictionModel



def test_flood_prediction_model():
    model1 = FloodPredictionModel.get_instance()
    model2 = FloodPredictionModel.get_instance()
    assert model1 is model2, "Singleton instance failed"

    try:
        model1.load_if_needed("../dashboard/dashboard/models/lstm_smote_cv.h5")
        assert model1.is_loaded, "Model should be loaded successfully"
    except Exception as e:
        assert False, f"Failed to load model: {e}"

    # Test prediction
    dummy_data = np.random.rand(10, 1, 12)
    result = model1.predict(dummy_data)
    assert result.shape[0] == 10, "Prediction result shape mismatch"

