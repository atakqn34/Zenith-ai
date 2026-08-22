import flet as ft
from google import genai
from google.genai import types

# --- GEMINI API KEY ---
GEMINI_API_KEY = "AQ.Ab8RN6JDJ4xOi2YWXfkpcqCG_2lXBCP9tdQ6Ov9cEtiqdumXIw"

def main(page: ft.Page):
    page.title = "Zenith AI"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 10
    
    # Gemini AI İstemcisi ve Sistem Talimatı
    client = genai.Client(api_key=GEMINI_API_KEY)
    
    # Sohbet Oturumu
    chat = client.chats.create(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(
            system_instruction="Sen Zenith AI adında gelişmiş, yardımsever, bilgili ve samimi bir yapay zeka asistanısın."
        )
    )

    selected_image_bytes = None

    chat_list = ft.ListView(
        expand=True,
        spacing=10,
        auto_scroll=True
    )

    def cihaz_komut_kontrol(komut):
        komut_lower = komut.lower()
        if "hey zenith" in komut_lower:
            return "Dinliyorum, sizin için buradayım!"
        elif "telefonu kilitle" in komut_lower or "ekranı kapat" in komut_lower:
            return "[SİSTEM]: Cihazı kilitleme komutu simüle edildi."
        elif "ekranı aç" in komut_lower or "kilidi aç" in komut_lower:
            return "[SİSTEM]: Ekran kilidi kaldırma komutu güvenlik duvarı nedeniyle engellendi."
        return None

    def on_file_selected(e: ft.FilePickerResultEvent):
        nonlocal selected_image_bytes
        if e.files and len(e.files) > 0:
            file_path = e.files[0].path
            with open(file_path, "rb") as f:
                selected_image_bytes = f.read()
            img_indicator.visible = True
            img_indicator.value = f"Görsel eklendi: {e.files[0].name}"
            page.update()

    file_picker = ft.FilePicker(on_result=on_file_selected)
    page.overlay.append(file_picker)

    img_indicator = ft.Text("", color=ft.Colors.GREEN_400, size=12, visible=False)

    def mesaj_gonder(e):
        nonlocal selected_image_bytes
        user_text = input_box.value.strip()
        
        if not user_text and not selected_image_bytes:
            return

        msg_controls = []
        if selected_image_bytes:
            msg_controls.append(ft.Text("🖼️ [Görsel Gönderildi]", color=ft.Colors.LIGHT_BLUE_200, italic=True))
        if user_text:
            msg_controls.append(ft.Text(user_text, color=ft.Colors.WHITE, selectable=True))

        chat_list.controls.append(
            ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Column(controls=msg_controls, spacing=5),
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
        img_indicator.visible = False
        page.update()

        loading_msg = ft.Row(
            controls=[
                ft.Container(
                    content=ft.Text("Zenith AI düşünüyor...", color=ft.Colors.GREY_400, italic=True),
                    bgcolor=ft.Colors.GREY_800,
                    padding=12,
                    border_radius=15,
                )
            ],
            alignment=ft.MainAxisAlignment.START
        )
        chat_list.controls.append(loading_msg)
        page.update()

        ozel_yanit = cihaz_komut_kontrol(user_text) if user_text else None

        try:
            if ozel_yanit:
                bot_reply = ozel_yanit
            elif selected_image_bytes:
                image_part = types.Part.from_bytes(
                    data=selected_image_bytes,
                    mime_type="image/jpeg"
                )
                prompt = user_text if user_text else "Bu görseli detaylıca analiz et ve açıkla."
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=[image_part, prompt]
                )
                selected_image_bytes = None
                bot_reply = response.text
            else:
                response = chat.send_message(user_text)
                bot_reply = response.text
        except Exception as err:
            bot_reply = f"Hata oluştu: {err}"

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

    input_box = ft.TextField(
        hint_text="Mesaj yazın veya fotoğraf yükleyin...",
        expand=True,
        border_radius=20,
        autofocus=True,
        on_submit=mesaj_gonder
    )
    
    attach_btn = ft.IconButton(
        icon=ft.Icons.IMAGE_ROUNDED,
        icon_color=ft.Colors.GREEN_400,
        on_click=lambda _: file_picker.pick_files(allow_multiple=False, file_type=ft.FilePickerFileType.IMAGE)
    )

    send_btn = ft.IconButton(
        icon=ft.Icons.SEND_ROUNDED,
        icon_color=ft.Colors.BLUE_400,
        on_click=mesaj_gonder
    )

    page.add(
        ft.AppBar(
            title=ft.Text("Zenith AI", weight=ft.FontWeight.BOLD),
            center_title=True,
            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST
        ),
        chat_list,
        img_indicator,
        ft.Row(controls=[attach_btn, input_box, send_btn])
    )

ft.app(target=main)

