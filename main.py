import flet as ft
import speech_recognition as sr
import tempfile
import os

def main(page: ft.Page):
    page.title = "VocalScribe"
    page.bgcolor = "#4D0213"
    page.padding = 20
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    uploaded_file_path = None

    # --- UI ELEMENTS ---
    transcription_text = ft.TextField(
        label="Audio Transcription",
        multiline=True,
        min_lines=5,
        read_only=True,
        width=500,
        bgcolor="#3b3f45",
        color="white"
    )

    status_text = ft.Text("", color="white")

    # --- FILE PICKER ---
    file_picker = ft.FilePicker()
    page.overlay.append(file_picker)

    def pick_file(e):
        file_picker.pick_files(allow_multiple=False)

    def on_file_selected(e):
        nonlocal uploaded_file_path

        if e.files:
            uploaded_file_path = e.files[0].path
            status_text.value = f"✅ Uploaded: {e.files[0].name}"
        else:
            status_text.value = "⚠️ No file selected"

        page.update()

    file_picker.on_result = on_file_selected

    # --- TRANSCRIBE ---
    def transcribe(e):
        if not uploaded_file_path:
            status_text.value = "Upload a file first!"
            page.update()
            return

        status_text.value = "🎧 Transcribing..."
        page.update()

        try:
            recognizer = sr.Recognizer()

            with sr.AudioFile(uploaded_file_path) as source:
                audio_data = recognizer.record(source)
                text = recognizer.recognize_google(audio_data)

            transcription_text.value = text
            status_text.value = "✅ Done!"

        except Exception as err:
            transcription_text.value = ""
            status_text.value = f"⚠️ Error: {err}"

        page.update()

    # --- DOWNLOAD TEXT ---
    def download(e):
        if not transcription_text.value.strip():
            status_text.value = "Nothing to download"
            page.update()
            return

        file_name = "transcription.txt"

        with open(file_name, "w", encoding="utf-8") as f:
            f.write(transcription_text.value)

        status_text.value = "📄 File saved as transcription.txt"
        page.update()

    # --- UI LAYOUT ---
    page.add(
        ft.Column(
            [
                ft.Text("🎙 VocalScribe", size=30, weight="bold", color="white"),

                ft.Container(
                    content=ft.Text("📁 Click here to upload audio file", color="black"),
                    bgcolor="#d2b49c",
                    padding=15,
                    border_radius=30,
                    alignment=ft.alignment.center,
                    on_click=pick_file,
                    width=400
                ),

                transcription_text,

                ft.Row(
                    [
                        ft.ElevatedButton("Transcribe", on_click=transcribe),
                        ft.ElevatedButton("Download as .TXT", on_click=download),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                ),

                status_text
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    ft.run(main, port=port)








# import flet as ft
# import speech_recognition as sr
# import os
#
#
# def main(page: ft.Page):
#     page.title = "VocalScribe"
#     page.bgcolor = "#4D0213"
#     page.padding = 20
#     page.vertical_alignment = ft.MainAxisAlignment.CENTER
#
#     uploaded_file_path = None
#
#     transcription_text = ft.TextField(
#         label="Audio Transcription",
#         multiline=True,
#         min_lines=5,
#         read_only=True,
#         expand=True
#     )
#
#     status_text = ft.Text("", color="WHITE")
#
#     # ---------------- FILE UPLOAD ----------------
#     def upload_result(e):
#         nonlocal uploaded_file_path
#
#         if e.files:
#             file = e.files[0]
#
#             # ✅ Use file path (works on Render)
#             uploaded_file_path = file.path
#
#             status_text.value = f"✅ Uploaded: {file.name}"
#         else:
#             status_text.value = "⚠️ No file selected"
#
#         page.update()
#
#     file_picker = ft.FilePicker()
#     file_picker.on_result = upload_result
#     page.overlay.append(file_picker)
#
#     # ---------------- TRANSCRIBE ----------------
#     def transcribe(e):
#         if not uploaded_file_path:
#             status_text.value = "Upload a file first!"
#             page.update()
#             return
#
#         status_text.value = "🎧 Transcribing..."
#         page.update()
#
#         try:
#             recognizer = sr.Recognizer()
#
#             # ✅ Only WAV files supported
#             with sr.AudioFile(uploaded_file_path) as source:
#                 audio_data = recognizer.record(source)
#                 text = recognizer.recognize_google(audio_data)
#
#             transcription_text.value = text
#             status_text.value = "✅ Done!"
#
#         except Exception as err:
#             transcription_text.value = ""
#             status_text.value = f"⚠️ Error: {err}"
#
#         page.update()
#
#     # ---------------- COPY ----------------
#     def copy_text(e):
#         if transcription_text.value.strip():
#             page.set_clipboard(transcription_text.value)
#             status_text.value = "📋 Copied to clipboard!"
#         else:
#             status_text.value = "Nothing to copy"
#         page.update()
#
#     # ---------------- UI ----------------
#     page.add(
#         ft.Text("🎙 VocalScribe", size=30, weight="bold"),
#
#         ft.ElevatedButton(
#             "Upload WAV Audio",
#             on_click=lambda _: file_picker.pick_files(
#                 allow_multiple=False,
#                 allowed_extensions=["wav"]   # ✅ ONLY WAV
#             )
#         ),
#
#         transcription_text,
#
#         ft.Row([
#             ft.ElevatedButton("Transcribe", on_click=transcribe),
#             ft.ElevatedButton("Copy Text", on_click=copy_text),
#         ]),
#
#         status_text
#     )
#
#
# # ---------------- RUN APP ----------------
# if __name__ == "__main__":
#     port = int(os.environ.get("PORT", 8550))
#
#     ft.run(
#         main,
#         port=port,
#         upload_dir="uploads"   # ✅ REQUIRED for file upload on Render
#     )


# import flet as ft
# import speech_recognition as sr
# import tempfile
#
# def main(page: ft.Page):
#     page.title = "PROJECT B"
#     page.bgcolor = "#4D0213"
#     page.padding = 20
#     page.vertical_alignment = ft.MainAxisAlignment.CENTER
#
#     uploaded_file_bytes = None
#
#     transcription_text = ft.TextField(
#         label="Audio Transcription",
#         multiline=True,
#         min_lines=5,
#         read_only=True,
#         expand=True
#     )
#
#     status_text = ft.Text("", color="WHITE")
#
#     # --- FILE UPLOAD ---
#     def upload_result(e):
#         nonlocal uploaded_file_bytes
#
#         if e.files:
#             file = e.files[0]
#
#             # Read file as bytes
#             uploaded_file_bytes = file.bytes
#             status_text.value = f"✅ Uploaded: {file.name}"
#         else:
#             status_text.value = "⚠️ No file selected"
#
#         page.update()
#
#     file_picker = ft.FilePicker(on_result=upload_result)
#     page.overlay.append(file_picker)
#
#     # --- TRANSCRIPTION ---
#     def transcribe(e):
#         if not uploaded_file_bytes:
#             status_text.value = "Upload a file first!"
#             page.update()
#             return
#
#         status_text.value = "🎧 Transcribing..."
#         page.update()
#
#         try:
#             recognizer = sr.Recognizer()
#
#             # Save temp file (needed for speech_recognition)
#             with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
#                 temp_audio.write(uploaded_file_bytes)
#                 temp_audio_path = temp_audio.name
#
#             with sr.AudioFile(temp_audio_path) as source:
#                 audio = recognizer.record(source)
#                 text = recognizer.recognize_google(audio)
#
#             transcription_text.value = text
#             status_text.value = "✅ Done!"
#
#         except Exception as err:
#             transcription_text.value = ""
#             status_text.value = f"⚠️ Error: {err}"
#
#         page.update()
#
#     # --- COPY TO CLIPBOARD ---
#     def download(e):
#         if transcription_text.value.strip():
#             page.set_clipboard(transcription_text.value)
#             status_text.value = "📋 Copied to clipboard!"
#         else:
#             status_text.value = "Nothing to copy"
#
#         page.update()
#
#     # --- UI ---
#     page.add(
#         ft.Text("🎙 VocalScribe", size=30, weight="bold"),
#
#         ft.ElevatedButton(
#             "Upload Audio",
#             on_click=lambda _: file_picker.pick_files(
#                 allow_multiple=False,
#                 allowed_extensions=["wav"]
#             )
#         ),
#
#         transcription_text,
#
#         ft.Row([
#             ft.ElevatedButton("Transcribe", on_click=transcribe),
#             ft.ElevatedButton("Copy Text", on_click=download),
#         ]),
#
#         status_text
#     )
#
# # --- RUN IN WEB BROWSER ---
# if __name__ == "__main__":
#     ft.run(main, view=ft.AppView.WEB_BROWSER)







# import flet as ft
# import speech_recognition as sr
# import tempfile
#
#
# def main(page: ft.Page):
#     page.title = "PROJECT B"
#     page.bgcolor = "#4D0213"
#     page.padding = 20
#     page.vertical_alignment = ft.MainAxisAlignment.CENTER
#
#     uploaded_file_bytes = None
#
#     transcription_text = ft.TextField(
#         label="Audio Transcription",
#         multiline=True,
#         min_lines=5,
#         read_only=True,
#         expand=True
#     )
#
#     status_text = ft.Text("", color="WHITE")
#
#     # --- FILE UPLOAD ---
#     def upload_result(e: ft.FilePickerResultEvent):
#         nonlocal uploaded_file_bytes
#
#         if e.files:
#             file = e.files[0]
#
#             # Read file as bytes
#             uploaded_file_bytes = file.bytes
#             status_text.value = f"✅ Uploaded: {file.name}"
#         else:
#             status_text.value = "⚠️ No file selected"
#
#         page.update()
#
#     file_picker = ft.FilePicker(on_result=upload_result)
#     page.overlay.append(file_picker)
#
#     # --- TRANSCRIPTION ---
#     def transcribe(e):
#         if not uploaded_file_bytes:
#             status_text.value = "Upload a file first!"
#             page.update()
#             return
#
#         status_text.value = "🎧 Transcribing..."
#         page.update()
#
#         try:
#             recognizer = sr.Recognizer()
#
#             # Save temp file (needed for speech_recognition)
#             with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
#                 temp_audio.write(uploaded_file_bytes)
#                 temp_audio_path = temp_audio.name
#
#             with sr.AudioFile(temp_audio_path) as source:
#                 audio = recognizer.record(source)
#                 text = recognizer.recognize_google(audio)
#
#             transcription_text.value = text
#             status_text.value = "✅ Done!"
#
#         except Exception as err:
#             transcription_text.value = ""
#             status_text.value = f"⚠️ Error: {err}"
#
#         page.update()
#
#     # --- DOWNLOAD ---
#     def download(e):
#         if transcription_text.value.strip():
#             page.set_clipboard(transcription_text.value)
#             status_text.value = "📋 Copied to clipboard!"
#         else:
#             status_text.value = "Nothing to copy"
#
#         page.update()
#
#     # --- UI ---
#     page.add(
#         ft.Text("🎙 VocalScribe", size=30, weight="bold"),
#
#         ft.ElevatedButton(
#             "Upload Audio",
#             on_click=lambda _: file_picker.pick_files(
#                 allow_multiple=False,
#                 allowed_extensions=["wav"]
#             )
#         ),
#
#         transcription_text,
#
#         ft.Row([
#             ft.ElevatedButton("Transcribe", on_click=transcribe),
#             ft.ElevatedButton("Copy Text", on_click=download),
#         ]),
#
#         status_text
#     )
#
#
# # IMPORTANT: enable web mode
# if __name__ == "__main__":
#     ft.run(main, view=ft.AppView.WEB_BROWSER)