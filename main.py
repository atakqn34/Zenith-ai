import flet as ft

def main(page: ft.Page):
    # Sayfa temel ayarları
    page.title = "Zenith-ai"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.bgcolor = ft.Colors.BLACK
    page.padding = 20

    # Başlık bileşeni
    title_text = ft.Text(
        "Zenith-ai Asistanı",
        size=24,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.WHITE,
        text_align=ft.TextAlign.CENTER
    )

    # Durum bilgisi bileşeni
    status_text = ft.Text(
        "Sistem Hazır ve Kararlı",
        size=14,
        color=ft.Colors.GREY_400,
        text_align=ft.TextAlign.CENTER
    )

    # Butona tıklama olayı
    def button_click(e):
        status_text.value = "Sistem Aktif, İşlem Başarılı! 🚀"
        status_text.color = ft.Colors.GREEN_400
        page.update()

    # Ana aksiyon butonu
    action_button = ft.ElevatedButton(
        text="Sistemi Başlat",
        on_click=button_click,
        color=ft.Colors.WHITE,
        bgcolor=ft.Colors.BLUE_900,
        width=200
    )

    # Ana ekran yerleşimi
    page.add(
        ft.Column(
            [
                title_text,
                ft.Container(height=10),
                status_text,
                ft.Container(height=30),
                action_button
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10
        )
    )

if __name__ == "__main__":
    ft.app(target=main)
