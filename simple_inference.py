import joblib
import pickle
import pandas as pd


if __name__ == "__main__":
    scaler_path = "dashboard/models/robust_scaler.pkl"
    with open(scaler_path, "rb") as f:
        scaler = pickle.load(f)
    model_path = "dashboard/models/random_forest_model.joblib"
    model = joblib.load(model_path)
    data_path = "dashboard/data/flood_inference_data.csv"
    data = pd.read_csv(data_path)
    df_scaled = data.copy()
    print(data.head())
    numerical_features = [
        "lon",
        "lat",
        "precip_1d",
        "precip_3d",
        "NDVI",
        "NDWI",
        "elevation",
        "slope",
        "aspect",
        "upstream_area",
        "TWI",
    ]
    model_feature = [
        "lon",
        "lat",
        "precip_1d",
        "precip_3d",
        "NDVI",
        "NDWI",
        "elevation",
        "slope",
        "aspect",
        "upstream_area",
        "TWI",
        "landcover",
    ]
    df_scaled[numerical_features] = scaler.transform(df_scaled[numerical_features])
    data_inference = df_scaled.drop(columns=["target"])
    model_predictions = model.predict(data_inference[model_feature])
    print("Model predictions:", model_predictions)
