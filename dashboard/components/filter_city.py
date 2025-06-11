import reflex as rx
from typing import List, Optional
def filter_sidebar(
    title: str = "Filter & Analisis",
    options: List[str] = None,
    select_placeholder: str = "Select an option...",
    select_default: Optional[str] = None,
    additional_content: Optional[rx.Component] = None,
    compact: bool = False,
) -> rx.Component:
    """
    Reusable filter sidebar component with card styling.
    """
    options = options or []
    
    title_size = "4" if compact else "5"
    padding = "1em" if compact else "1.5em"
    text_size = "sm" if compact else None
    select_size = "1" if compact else "2"
    
    content = [
        rx.heading(
            title,
            size=title_size,
            margin_bottom="0.75em" if not compact else "0.5em",
            color_scheme="gray",
        ),
    ]
    
    if options:
        if compact:
            content.append(
                rx.hstack(
                    rx.text("Choose Regency", weight="medium", font_size=text_size),
                    rx.select(
                        options,
                        placeholder=select_placeholder,
                        default_value=select_default,
                        flex="1",
                        size=select_size,
                    ),
                    spacing="3",
                    align_items="center",
                    width="100%",
                )
            )
        else:
            content.extend([
                rx.text("Choose Regency", weight="medium", margin_bottom="0.25em"),
                rx.select(
                    options,
                    placeholder=select_placeholder,
                    default_value=select_default,
                    width="100%",
                    size=select_size,
                ),
            ])
    
    if additional_content:
        if not compact:
            content.append(rx.divider(margin_y="0.5em"))
        content.append(additional_content)
    
    if not compact:
        content.append(rx.spacer())
    
    return rx.card(
        rx.vstack(
            *content,
            spacing="4" if not compact else "2",
            align_items="stretch",
            width="100%",
            height="100%",
        ),
        padding=padding,
        width="100%",
        height=["auto", "auto", "100%", "100%"], 
        variant="classic",
        size="2" if not compact else "1",
        box_shadow="0 2px 8px rgba(0, 0, 0, 0.1)",
        _hover={
            "box_shadow": "0 4px 12px rgba(0, 0, 0, 0.15)",
            "transition": "box-shadow 0.2s ease-in-out",
        },
    )