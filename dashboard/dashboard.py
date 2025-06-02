"""Welcome to Reflex!."""

# Import all the pages.
import reflex as rx

from . import styles
from .pages import *
# from .backend.map import MAPS
# Create the app.
app = rx.App(
    style=styles.base_style,
    stylesheets=styles.base_stylesheets,
    
    
)
