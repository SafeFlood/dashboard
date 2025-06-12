import reflex as rx
from typing import Optional


def responsive_two_column_layout(
    main_content: rx.Component,
    sidebar_content: rx.Component,
    main_width: str = "70%",
    sidebar_width: str = "30%",
    spacing: str = "0",
    height: str = "100%",
    min_height: str = "600px",
    sidebar_bg: Optional[str] = None,
    sidebar_border: bool = True,
    mobile_stack: bool = True,
) -> rx.Component:
    """
    Responsive two-column layout component.
    
    Args:
        main_content: Main content component
        sidebar_content: Sidebar content component
        main_width: Width of main content area (default: "70%")
        sidebar_width: Width of sidebar area (default: "30%")
        spacing: Spacing between columns (default: "0")
        height: Height of the layout (default: "100%")
        min_height: Minimum height (default: "600px")
        sidebar_bg: Background color for sidebar
        sidebar_border: Whether to show sidebar border (default: True)
        mobile_stack: Whether to stack on mobile (default: True)
    """
    sidebar_bg = sidebar_bg or rx.color("gray", 1)
    
    # Desktop Layout
    desktop_layout = rx.hstack(
        rx.box(
            main_content,
            width=main_width,
            height="100%",
            overflow="hidden",
        ),
        rx.box(
            sidebar_content,
            width=sidebar_width,
            height="100%",
            padding_left="0.5em",
            bg=sidebar_bg,
        ),
        spacing=spacing,
        width="100%",
        align_items="stretch",
        height=height,
        min_height=min_height,
        display=["none", "none", "flex", "flex"] if mobile_stack else "flex",
    )
    
    # Mobile Layout (if enabled)
    mobile_layout = None
    if mobile_stack:
        mobile_layout = rx.vstack(
            rx.box(
                sidebar_content,
                width="100%",
                bg=sidebar_bg,
                border_bottom=f"1px solid {rx.color('gray', 4)}" if sidebar_border else None,
            ),
            rx.box(
                main_content,
                width="100%",
                flex="1",
                overflow="hidden",
            ),
            spacing="0",
            width="100%",
            height="100vh",
            display=["flex", "flex", "none", "none"],
        )
    
    if mobile_layout:
        return rx.box(desktop_layout, mobile_layout, width="100%", height="100%")
    else:
        return desktop_layout


def map_display_area(
    map_component: rx.Component,
    padding: str = "0.1em",
    mobile_padding: str = "1em",
) -> rx.Component:
    """
    Reusable map display area component.
    
    Args:
        map_component: The map component to display
        padding: Padding for desktop view
        mobile_padding: Padding for mobile view
    """
    return rx.box(
        rx.box(
            map_component,
            padding=padding,
            height="100%",
            overflow="hidden",
            display=["none", "none", "block", "block"],  # Desktop
        ),
        rx.box(
            map_component,
            padding=mobile_padding,
            height="100%",
            overflow="hidden",
            display=["block", "block", "none", "none"],  # Mobile
        ),
        width="100%",
        height="100%",
    )