import reflex as rx
from typing import List, Optional
from ..backend import FloodPredictionModel, MapState, get_ground_truth_targets


class FilterSidebarState(rx.State):
    is_loading: bool = False
    progress_text: str = "Loading..."
    value: str = "target"

    @rx.event
    def change_loading_state(self, is_loading: bool):
        self.is_loading = is_loading

    @rx.event
    def show_marker(self, selected_value: str | list[str]):
        self.change_loading_state(True)
        if isinstance(selected_value, list):
            selected_value = selected_value[0] if selected_value else ""
        self.value = selected_value
        if selected_value == "target":
            print("Loading ground truth coordinates...")
            self.progress_text = "Loading Ground Truth Coordinates..."
            
        elif selected_value == "predict":
            print("Loading flood prediction coordinates...")
            self.progress_text = "Loading Flood Prediction Coordinates..."
            yield MapState.set_flood_prediction_coordinates
        print(f"Selected value: {self.value}")
        self.change_loading_state(False)


def filter_sidebar(
    title: str = "Filter & Analisis",
    additional_content: Optional[rx.Component] = None,
    compact: bool = False,
) -> rx.Component:
    """
    Reusable filter sidebar component with card styling.
    """

    title_size = "4" if compact else "5"
    padding = "1em" if compact else "1.5em"
    text_size = "sm" if compact else None

    content = [
        rx.hstack(
            rx.heading(
                title,
                size=title_size,
                margin_bottom="0" if not compact else "0",
                color_scheme="gray",
            ),
            rx.tooltip(
                rx.icon(
                    "info",
                    size=16,
                    color="gray",
                    cursor="pointer",
                ),
                content="Data yang digunakan adalah data validation pada tanggal 10-12-2003",
            ),
            align_items="center",
            spacing="2",
            margin_bottom="0.75em" if not compact else "0.5em",
        ),
    ]

    if compact:
        content.append(
            rx.vstack(
                rx.text("Choose Mode", weight="medium", font_size=text_size),
                rx.segmented_control.root(
                    rx.segmented_control.item("Ground Truth", value="target"),
                    rx.segmented_control.item("Predict", value="predict"),
                    on_change=FilterSidebarState.show_marker,
                    value=FilterSidebarState.value,
                    width="100%",
                ),
                rx.cond(
                    FilterSidebarState.is_loading,
                    rx.hstack(
                        rx.spinner(size="1"),
                        rx.text(
                            FilterSidebarState.progress_text,
                            font_size="sm",
                            color="gray",
                        ),
                        align_items="center",
                        spacing="2",
                        justify_content="center",
                        margin_top="0.5em",
                    ),
                ),
                spacing="2",
                align_items="stretch",
                width="100%",
            )
        )
    else:
        content.extend(
            [
                rx.text("Choose Mode", weight="medium", margin_bottom="0.25em"),
                rx.segmented_control.root(
                    rx.segmented_control.item("Ground Truth", value="target"),
                    rx.segmented_control.item("Predict", value="predict"),
                    on_change=FilterSidebarState.show_marker,
                    value=FilterSidebarState.value,
                    width="100%",
                    size="2",
                ),
                rx.cond(
                    FilterSidebarState.is_loading,
                    rx.hstack(
                        rx.spinner(size="2"),
                        rx.text(
                            FilterSidebarState.progress_text,
                            font_size="sm",
                            color="gray",
                        ),
                        align_items="center",
                        spacing="2",
                        justify_content="center",
                        margin_top="0.5em",
                    ),
                ),
            ]
        )

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
