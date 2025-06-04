import reflex as rx
from ..templates import template
from ..backend import FloodPredictionModel

model = FloodPredictionModel.get_instance()

@template(
    title="FloodSense",
    description="FloodSense is a web application that provides real-time flood monitoring and alerts.",
    route="/floodsense",
    on_load=model.load_if_needed("../dashboard/dashboard/models/lstm_smote_cv.h5") 
)
def floodsense():

    return f"Hello, FloodSense! {model.is_loaded}"