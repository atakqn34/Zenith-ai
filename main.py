import flet as ft
from google import genai

# --- GEMINI API KEY ---
GEMINI_API_KEY = "BURAYA_GEMINI_API_KEYINI_YAZ"

def main(page: ft.Page):
    page.title = "Zenith AI"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 10
    
    # Gemini AI İstemcisi
    client = genai.Client(api_key=GEMINI_API_KEY)
    chat = client.chats.create(model="gemini-2.5-flash")

    # Mesaj Liste Kutusu
    chat_list = ft.ListView(
        expand=True,
        spacing=10,
        auto_scroll=True
    )

    def mesaj_gonder(e):
        user_text = input_box.value.strip()
        if not user_text:
            return

        # Kullanıcı Mesajını Ekrana Ekle
        chat_list.controls.append(
            ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Text(user_text, color=ft.Colors.WHITE, selectable=True),
                        bgcolor=ft.Colors.BLUE_600,
                        padding=12,
                        border_radius=15,
                        width=280
                    )
                ],
                alignment=ft.MainAxisAlignment.END
            )
        )
        
        input_box.value = ""
        page.update()

        # Düşünüyor Balonu
        loading_msg = ft.Row(
            controls=[
                ft.Container(
                    content=ft.Text("Yapay Zeka düşünüyor...", color=ft.Colors.GREY_400, italic=True),
                    bgcolor=ft.Colors.GREY_800,
                    padding=12,
                    border_radius=15,
                )
            ],
            alignment=ft.MainAxisAlignment.START
        )
        chat_list.controls.append(loading_msg)
        page.update()

        try:
            # Gemini'den Cevap Al
            response = chat.send_message(user_text)
            bot_reply = response.text
        except Exception as err:
            bot_reply = f"Hata oluştu: {err}"

        # Düşünüyor Balonunu Kaldır ve Cevabı Ekle
        chat_list.controls.remove(loading_msg)
        chat_list.controls.append(
            ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Text(bot_reply, color=ft.Colors.WHITE, selectable=True),
                        bgcolor=ft.Colors.GREY_800,
                        padding=12,
                        border_radius=15,
                        width=280
                    )
                ],
                alignment=ft.MainAxisAlignment.START
            )
        )
        page.update()

    # Alt Giriş Alanı
    input_box = ft.TextField(
        hint_text="Bir şeyler yazın...",
        expand=True,
        border_radius=20,
        autofocus=True,
        on_submit=mesaj_gonder
    )
    
    send_btn = ft.IconButton(
        icon=ft.Icons.SEND_ROUNDED,
        icon_color=ft.Colors.BLUE_400,
        on_click=mesaj_gonder
    )

    # Arayüz Düzeni
    page.add(
        ft.AppBar(
            title=ft.Text("Zenith AI", weight=ft.FontWeight.BOLD),
            center_title=True,
            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST
        ),
        chat_list,
        ft.Row(controls=[input_box, send_btn])
    )

ft.app(target=main)
