import os
import reflex as rx
from ..templates import template
from ..backend import FloodPredictionModel
import os
from ..views.map_display import south_sulawesi_map_display
from ..components import filter_sidebar
from ..layout import map_display_area, responsive_two_column_layout
model = FloodPredictionModel.get_instance()



@template(
    title="FloodSense",
    description="FloodSense is a web application that provides real-time flood monitoring and alerts.",
    route="/floodsense",
    on_load=model.load_if_needed(f"{os.getcwd()}/dashboard/models/lstm_smote_cv.h5"),
)
def floodsense():
    # Main map content
    main_content = map_display_area(
        map_component=south_sulawesi_map_display(),
        padding="0em",
        mobile_padding="1em",
    )
    
    # Desktop sidebar
    desktop_sidebar = filter_sidebar(
        title="Flood Prediction",
        compact=False,
    )
    
    mobile_sidebar = filter_sidebar(
        title="Flood Prediction", 
        compact=True,
    )
    
    # Combine both sidebars for responsive behavior
    sidebar_content = rx.box(
        rx.box(
            desktop_sidebar,
            display=["none", "none", "block", "block"],  
        ),
        rx.box(
            mobile_sidebar,
            display=["block", "block", "none", "none"],  
        ),
        width="100%",
        height="100%",
    )
    
    return responsive_two_column_layout(
        main_content=main_content,
        sidebar_content=sidebar_content,
        main_width="70%",
        sidebar_width="30%",
        height="100%",
        min_height="600px",
        sidebar_bg=rx.color("gray", 1),
        sidebar_border=True,
        mobile_stack=True,
    )
