import reflex as rx
from ..templates import template
from ..backend import FloodPredictionModel

model = FloodPredictionModel.get_instance()

# Placeholder untuk komponen peta sebenarnya.
# Anda bisa menggantinya dengan rx.html, rx.iframe untuk peta eksternal,
# atau komponen peta kustom jika Anda memilikinya.
def map_area_placeholder() -> rx.Component:
    return rx.center(
        # Teks "Maps" dan "Beloved Marten" seperti pada gambar Anda
        rx.vstack(
            rx.text("Maps", font_size="2.5em", weight="bold", color_scheme="gray"),
            rx.text(
                "Beloved Marten", 
                font_size="0.8em", 
                color_scheme="orange", # Sesuai warna pada gambar
                bg="rgba(255, 228, 196, 0.5)", # Latar belakang oranye transparan
                padding_x="0.5em",
                border_radius="sm"
            ),
            align="center",
            spacing="1"
        ),
        border=f"1px solid {rx.color('gray', 4)}", # Garis batas halus
        border_radius="lg", # Sudut yang lebih membulat
        width="100%",
        height="100%", # Mengisi tinggi parent vstack
        flex_grow=1,   # Memastikan komponen ini tumbuh mengisi ruang
        bg=rx.color('gray', 1) # Latar belakang sangat terang untuk area peta
    )

# Komponen untuk form input prediksi
def prediction_input_form() -> rx.Component:
    return rx.vstack(
        rx.heading("Form Prediksi Banjir", size="4", margin_bottom="0.5em", color_scheme="gray"),
        
        rx.text("Curah Hujan (mm):", size="2", margin_bottom="0.1em"),
        rx.input(
            value="",
            # on_change=FloodPredictionState.handle_curah_hujan_change,
            placeholder="e.g., 50.5",
            width="100%",
            step=0.1,
            type="number",
            min_=0,
        ),
        
        rx.text("Ketinggian Air Sungai (cm):", size="2", margin_top="0.75em", margin_bottom="0.1em"),
        rx.input(
            value="",
            # on_change=FloodPredictionState.handle_ketinggian_air_change,
            placeholder="e.g., 120",
            width="100%",
            step=1,
            type="number",
            min_=0,
        ),

        rx.text("Durasi Hujan Terakhir (jam):", size="2", margin_top="0.75em", margin_bottom="0.1em"),
        rx.input(
            value="",
            # on_change=FloodPredictionState.handle_durasi_hujan_change,
            placeholder="e.g., 3",
            width="100%",
            step=0.5,
            type="number",
            min_=0,
        ),
        
        rx.button(
            "Prediksi Sekarang", 
            # on_click="",
            # is_loading=FloodPredictionState.is_processing,
            width="100%", 
            margin_top="1.5em",
            margin_bottom="1.5em",
            size="2",
            color_scheme="blue"
        ),

        # Menampilkan hasil prediksi
        # rx.cond(
        #     # FloodPredictionState.hasil_prediksi != "",
        #     rx.box(
        #         rx.text("Hasil Prediksi:", weight="bold", size="3", margin_bottom="0.25em"),
        #         rx.text("FloodPredictionState.hasil_prediksi", size="3"),
        #         padding="1em",
        #         margin_top="1em",
        #         border=f"1px solid {rx.color('blue', 6)}",
        #         border_radius="md",
        #         width="100%",
        #         bg=rx.color('blue', 2)
        #     )
        # ),
        spacing="3",
        width="100%",
        align_items="stretch", # Memastikan semua elemen form merentang penuh
        # margin_bottom="6em"
    )

@template(
    title="FloodSense",
    description="FloodSense is a web application that provides real-time flood monitoring and alerts.",
    route="/floodsense",
    on_load=model.load_if_needed("../dashboard/dashboard/models/lstm_smote_cv.h5") 
)
def floodsense():
    return rx.hstack(
        # 1. Area Konten Utama (untuk "Maps")
        rx.vstack(
            map_area_placeholder(),
            # Anda bisa menambahkan elemen lain di bawah peta jika perlu
            spacing="4",      # Jarak antar elemen di vstack ini
            overflow_y="hidden",
            padding="1.5em",  # Padding di sekitar area peta
            align_items="stretch", # Membuat children (map_area_placeholder) merentang penuh
            width="70%",      # Proporsi lebar untuk area peta (sesuaikan jika perlu)
            height="100%",    # Mengisi tinggi hstack induk
        ),
        # 2. Sidebar Kanan (untuk kontrol)
        rx.vstack(
            rx.heading("Filter & Analisis", size="5", margin_bottom="0.75em", color_scheme="gray"),
            
            rx.text("Choose Regency", weight="medium", margin_bottom="0.25em"),
            rx.select(
                ["Bantaeng", "Barru", "Bone", "Bulukumba", "Enrekang", "Gowa", "Jeneponto", "Kepulauan Selayar", "Luwu", "Luwu Timur", "Luwu Utara", "Maros", "Pinrang", "Sidenreng Rappang", "Soppeng", "Takalar", "Tana Toraja", "Toraja Utara", "Wajo", "Sidrap"], # Contoh daftar kabupaten
                placeholder="Pilih Kabupaten/Kota...",
                default_value="Aceh Besar", # Nilai default (opsional)
                width="100%",
                size="2", # Ukuran select: "1" (kecil), "2" (sedang), "3" (besar)
            ),
            
            rx.divider(margin_y="1.5em"), # Pemisah visual
            
            rx.text("Mode Tampilan", weight="medium", margin_bottom="0.25em"),
            rx.segmented_control.root(
                rx.segmented_control.item("Predict", value="predict"),
                rx.segmented_control.item("Real-Time", value="real"), # Mengganti "Real" menjadi "Real-Time" agar lebih jelas
                default_value="real",
                width="100%",
                size="2",
            ),
            
            # Anda bisa menambahkan kontrol lain di sini
            # rx.button("Terapkan Filter", width="100%", margin_top="1.5em", size="2"),

            rx.divider(margin_y="0.5em"), # Pemisah sebelum form prediksi

            # Menambahkan form input prediksi di sini
            prediction_input_form(),

            rx.spacer(), # Mendorong elemen berikutnya ke bawah jika ada
            
            # Contoh tambahan: Tombol aksi atau informasi
            # rx.box(
            #     rx.text("Status: Monitoring Aktif", size="1", color_scheme="green"),
            #     padding="0.5em",
            #     border=f"1px solid {rx.color('green', 4)}",
            #     border_radius="md",
            #     width="100%",
            #     text_align="center"
            # ),

            spacing="4",        # Jarak antar elemen di sidebar kanan
            padding="1.5em",    # Padding di sekitar sidebar kanan
            align_items="stretch", # Membuat children (select, segmented_control) merentang penuh
            width="30%",        # Proporsi lebar untuk sidebar kanan
            height="100%",      # Mengisi tinggi hstack induk
            border_left=f"1px solid {rx.color('gray', 4)}", # Garis pemisah kiri
            bg=rx.color('gray', 1) # Warna latar belakang sedikit berbeda untuk sidebar
        ),
        spacing="0", # Tidak ada jarak antara area peta dan sidebar kanan
        width="100%",
        align_items="stretch", # Membuat vstack anak merentang setinggi hstack
        # Tinggi keseluruhan akan diatur oleh template
        # Biasanya, template akan membuat konten halaman mengisi ruang yang tersedia.
        # Misalnya, bisa menggunakan min_height="calc(100vh - VAR_NAVBAR_HEIGHT)" jika navbar punya tinggi tetap.
        # Jika template Anda sudah menangani ini, maka tinggi 100% di sini akan relatif terhadap parentnya.
        # height="calc(100vh - 60px)" # Contoh: Asumsi tinggi navbar/header adalah 60px. Sesuaikan!
        height = "100%"                            # Atau, jika template Anda adalah flex container yang mengisi viewport,
                                    # Anda mungkin tidak perlu set tinggi eksplisit di sini.
                                    # Anda bisa coba tanpa ini dulu dan lihat bagaimana template menanganinya.
    )

    return f"Hello, FloodSense! {model.is_loaded}"
