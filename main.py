import os
import flet as ft
from google import genai
from google.genai import types

# Gemini API Anahtarını buraya ekliyoruz
# (Kendi API anahtarını buraya yazabilirsin)
GEMINI_API_KEY = "BURAYA_API_ANAHTARINI_YAZ"

def main(page: ft.Page):
    page.title = "Zenith AI"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 10
    page.vertical_alignment = ft.MainAxisAlignment.END

    # Gemini İstemcisini Başlatma
    client = None
    chat_session = None
    
    try:
        if GEMINI_API_KEY and GEMINI_API_KEY != "BURAYA_API_ANAHTARINI_YAZ":
            client = genai.Client(api_key=GEMINI_API_KEY)
            chat_session = client.chats.create(model="gemini-2.5-flash")
    except Exception as e:
        print(f"API Başlatma Hatası: {e}")

    # Seçilen görselin verilerini tutacak değişken
    selected_image_bytes = None
    selected_image_name = ft.Text("Görsel seçilmedi", size=12, italic=True, color=ft.colors.GREY_400)

    # Mesajların listeleneceği alan
    chat_list = ft.ListView(expand=True, spacing=10, auto_scroll=True)

    # Görsel Seçildiğinde Çalışacak Fonksiyon
    def on_file_selected(e: ft.FilePickerResultEvent):
        nonlocal selected_image_bytes
        if e.files and len(e.files) > 0:
            file_path = e.files[0].path
            selected_image_name.value = f"Seçilen: {e.files[0].name}"
            selected_image_name.update()
            
            try:
                with open(file_path, "rb") as f:
                    selected_image_bytes = f.read()
            except Exception as ex:
                selected_image_name.value = "Görsel okunamadı!"
                selected_image_name.update()

    # FilePicker Nesnesi ve OVERLAY Hatası Çözümü (page.overlay içine ekleniyor)
    file_picker = ft.FilePicker(on_result=on_file_selected)
    page.overlay.append(file_picker)
    page.update()

    # Mesaj Gönderme Fonksiyonu
    def send_message(e):
        user_text = message_input.value.strip()
        if not user_text and not selected_image_bytes:
            return

        # Kullanıcı mesajını ekrana ekle
        chat_list.controls.append(
            ft.Row(
                [
                    ft.Container(
                        content=ft.Text(user_text if user_text else "[Görsel Gönderildi]", color=ft.colors.WHITE),
                        bgcolor=ft.colors.BLUE_900,
                        padding=10,
                        border_radius=8,
                        max_width=250
                    )
                ],
                alignment=ft.MainAxisAlignment.END
            )
        )
        
        current_input = user_text
        message_input.value = ""
        message_input.update()
        chat_list.update()

        # Asistanın yanıt alanı (Yükleniyor efekti için)
        ai_response_text = ft.Text("Düşünüyor...", color=ft.colors.WHITE)
        ai_container = ft.Container(
            content=ai_response_text,
            bgcolor=ft.colors.GREY_800,
            padding=10,
            border_radius=8,
            max_width=250
        )
        
        ai_row = ft.Row([ai_container], alignment=ft.MainAxisAlignment.START)
        chat_list.controls.append(ai_row)
        chat_list.update()

        # Gemini'ye istek atma
        try:
            if not client or not chat_session:
                ai_response_text.value = "Hata: API anahtarı tanımlanmamış!"
                ai_container.update()
                return

            contents = []
            if selected_image_bytes:
                image_part = types.Part.from_bytes(
                    data=selected_image_bytes,
                    mime_type="image/jpeg",
                )
                contents.append(image_part)
                # Gönderildikten sonra sıfırla
                selected_image_bytes = None
                selected_image_name.value = "Görsel seçilmedi"
                selected_image_name.update()

            if current_input:
                contents.append(current_input)

            # Gemini'den yanıt al
            response = chat_session.send_message(contents)
            ai_response_text.value = response.text
        except Exception as ex:
            ai_response_text.value = f"Bir hata oluştu: {str(ex)}"
        
        ai_container.update()

    # Giriş ve Buton Bileşenleri
    message_input = ft.TextField(
        hint_text="Mesajınızı yazın...",
        expand=True,
        border_radius=8,
        on_submit=send_message
    )

    upload_btn = ft.IconButton(
        icon=ft.icons.IMAGE,
        tooltip="Görsel Seç",
        on_click=lambda _: file_picker.pick_files(allowed_extensions=["png", "jpg", "jpeg"])
    )

    send_btn = ft.IconButton(
        icon=ft.icons.SEND,
        tooltip="Gönder",
        on_click=send_message
    )

    # Arayüz Yerleşimi
    page.add(
        chat_list,
        selected_image_name,
        ft.Row([upload_btn, message_input, send_btn], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
    )

ft.app(target=main)

