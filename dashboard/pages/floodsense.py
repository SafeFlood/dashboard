import os
import reflex as rx
from ..templates import template
from ..backend import FloodPredictionModel
from ..views.map_display import south_sulawesi_map_display
from ..components import filter_sidebar
from ..layout import map_display_area, responsive_two_column_layout
model = FloodPredictionModel.get_instance()


# @template(
#     title="FloodSense",
#     description="FloodSense is a web application that provides real-time flood monitoring and alerts.",
#     route="/floodsense",
#     on_load=model.load_if_needed(f"{os.getcwd()}/dashboard/models/lstm_smote_cv.h5"),
# )
# def floodsense():
#     return rx.hstack(
#         # 1. Area Konten Utama (untuk "Maps")
#         rx.vstack(
#             south_sulawesi_map_display(),
#             # Anda bisa menambahkan elemen lain di bawah peta jika perlu
#             spacing="4",  # Jarak antar elemen di vstack ini
#             overflow_y="hidden",
#             padding="1.5em",  # Padding di sekitar area peta
#             align_items="stretch",  # Membuat children (map_area_placeholder) merentang penuh
#             width="70%",  # Proporsi lebar untuk area peta (sesuaikan jika perlu)
#             height="100%",  # Mengisi tinggi hstack induk
#         ),
#         rx.vstack(
#             rx.heading(
#                 "Filter & Analisis",
#                 size="5",
#                 margin_bottom="0.75em",
#                 color_scheme="gray",
#             ),
#             rx.text("Choose Regency", weight="medium", margin_bottom="0.25em"),
#             rx.select(
#                 [
#                     "Bantaeng",
#                     "Barru",
#                     "Bone",
#                     "Bulukumba",
#                     "Enrekang",
#                     "Gowa",
#                     "Jeneponto",
#                     "Kepulauan Selayar",
#                     "Luwu",
#                     "Luwu Timur",
#                     "Luwu Utara",
#                     "Maros",
#                     "Pinrang",
#                     "Sidenreng Rappang",
#                     "Soppeng",
#                     "Takalar",
#                     "Tana Toraja",
#                     "Toraja Utara",
#                     "Wajo",
#                     "Sidrap",
#                 ],
#                 placeholder="Pilih Kabupaten/Kota...",
#                 default_value="Aceh Besar",
#                 width="100%",
#                 size="2",
#             ),
#             rx.divider(margin_y="0.5em"),
#             rx.spacer(),
#             spacing="4",  # Jarak antar elemen di sidebar kanan
#             padding="1.5em",  # Padding di sekitar sidebar kanan
#             align_items="stretch",  # Membuat children (select, segmented_control) merentang penuh
#             width="30%",  # Proporsi lebar untuk sidebar kanan
#             height="100%",  # Mengisi tinggi hstack induk
#             border_left=f"1px solid {rx.color('gray', 4)}",  # Garis pemisah kiri
#             bg=rx.color(
#                 "gray", 1
#             ),  # Warna latar belakang sedikit berbeda untuk sidebar
#         ),
#         spacing="0",  # Tidak ada jarak antara area peta dan sidebar kanan
#         width="100%",
#         align_items="stretch",  # Membuat vstack anak merentang setinggi hstack
#         # Tinggi keseluruhan akan diatur oleh template
#         # Biasanya, template akan membuat konten halaman mengisi ruang yang tersedia.
#         # Misalnya, bisa menggunakan min_height="calc(100vh - VAR_NAVBAR_HEIGHT)" jika navbar punya tinggi tetap.
#         # Jika template Anda sudah menangani ini, maka tinggi 100% di sini akan relatif terhadap parentnya.
#         # height="calc(100vh - 60px)" # Contoh: Asumsi tinggi navbar/header adalah 60px. Sesuaikan!
#         height="100%",  # Atau, jika template Anda adalah flex container yang mengisi viewport,
#         # Anda mungkin tidak perlu set tinggi eksplisit di sini.
#         # Anda bisa coba tanpa ini dulu dan lihat bagaimana template menanganinya.
#     )


# Configuration constants
REGENCY_OPTIONS = [
    "Bantaeng",
    "Barru", 
    "Bone",
    "Bulukumba",
    "Enrekang",
    "Gowa",
    "Jeneponto",
    "Kepulauan Selayar",
    "Luwu",
    "Luwu Timur",
    "Luwu Utara",
    "Maros",
    "Pinrang",
    "Sidenreng Rappang",
    "Soppeng",
    "Takalar",
    "Tana Toraja",
    "Toraja Utara",
    "Wajo",
    "Sidrap",
]


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
        padding="1.5em",
        mobile_padding="1em",
    )
    
    # Desktop sidebar
    desktop_sidebar = filter_sidebar(
        title="Filter & Analisis",
        options=REGENCY_OPTIONS,
        select_placeholder="Pilih Kabupaten/Kota...",
        select_default="Aceh Besar",
        compact=False,
    )
    
    mobile_sidebar = filter_sidebar(
        title="Filter & Analisis", 
        options=REGENCY_OPTIONS,
        select_placeholder="Pilih Kabupaten/Kota...",
        select_default="Aceh Besar",
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