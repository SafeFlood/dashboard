import reflex as rx
from ..templates import template

@template(
    title="FloodSense",
    description="FloodSense is a web application that provides real-time flood monitoring and alerts.",
    route="/floodsense",
    
)
def floodsense():
    return "Hello, FloodSense!"