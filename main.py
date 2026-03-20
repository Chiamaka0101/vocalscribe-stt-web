import flet as ft
import speech_recognition as sr
import tempfile
import os


def main(page: ft.Page):
    # --- PAGE SETTINGS ---
    page.title = "VocalScribe"
    page.bgcolor = "#4D0213"
    page.padding = 20
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    recorded_audio = None  # Will store recorded audio bytes

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

    # --- AUDIO RECORDER CALLBACK ---
    def on_record_complete(e):
        """
        This function runs when recording stops.
        It stores the recorded audio bytes.
        """
        nonlocal recorded_audio

        recorded_audio = e.data  # audio bytes from browser
        status_text.value = "✅ Audio recorded successfully!"
        page.update()

    # --- AUDIO RECORDER CONTROL ---
    recorder = ft.AudioRecorder(
        on_stop=on_record_complete  # trigger when recording stops
    )

    # --- TRANSCRIBE FUNCTION ---
    def transcribe(e):
        """
        Converts recorded audio into text using SpeechRecognition.
        """
        nonlocal recorded_audio

        if not recorded_audio:
            status_text.value = "⚠️ Please record audio first!"
            page.update()
            return

        status_text.value = "🎧 Transcribing..."
        page.update()

        try:
            recognizer = sr.Recognizer()

            # Save recorded audio to a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
                temp_audio.write(recorded_audio)
                temp_audio_path = temp_audio.name

            # Process audio file
            with sr.AudioFile(temp_audio_path) as source:
                audio_data = recognizer.record(source)
                text = recognizer.recognize_google(audio_data)

            transcription_text.value = text
            status_text.value = "✅ Transcription complete!"

            # Clean up temp file
            os.remove(temp_audio_path)

        except Exception as err:
            transcription_text.value = ""
            status_text.value = f"⚠️ Error: {err}"

        page.update()

    # --- UI LAYOUT ---
    page.add(
        ft.Column(
            [
                # App Title
                ft.Text("🎙 VocalScribe", size=30, weight="bold", color="white"),

                # Record Audio Button (Styled like your upload button)
                ft.Container(
                    content=ft.Text("🎤 Click to Record Audio", color="black"),
                    bgcolor="#d2b49c",
                    padding=15,
                    border_radius=30,
                    alignment=ft.alignment.center,
                    on_click=lambda e: recorder.start_recording(),
                    width=400
                ),

                # Stop Recording Button
                ft.ElevatedButton(
                    "Stop Recording",
                    on_click=lambda e: recorder.stop_recording()
                ),

                # Hidden recorder control (required for functionality)
                recorder,

                # Transcription output box
                transcription_text,

                # Transcribe button
                ft.ElevatedButton("Transcribe", on_click=transcribe),

                # Status messages
                status_text
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )


# --- ENTRY POINT ---
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    ft.run(main, port=port)








#LATEST CORRECTION BY CHAT#

# import flet as ft
# import speech_recognition as sr
# import tempfile
# import os
#
#
# def main(page: ft.Page):
#     page.title = "VocalScribe"
#     page.bgcolor = "#4D0213"
#     page.padding = 20
#     page.vertical_alignment = ft.MainAxisAlignment.CENTER
#     page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
#
#     uploaded_file = None
#
#     # --- UI ELEMENTS ---
#     transcription_text = ft.TextField(
#         label="Audio Transcription",
#         multiline=True,
#         min_lines=5,
#         read_only=True,
#         width=500,
#         bgcolor="#3b3f45",
#         color="white"
#     )
#
#     status_text = ft.Text("", color="white")
#
#     # --- FILE PICKER (WEB SAFE) ---
#     def on_upload(e: ft.FilePickerResultEvent):
#         nonlocal uploaded_file
#
#         if e.files:
#             uploaded_file = e.files[0]
#             status_text.value = f"✅ Uploaded: {uploaded_file.name}"
#         else:
#             status_text.value = "⚠️ No file selected"
#
#         page.update()
#
#     file_picker = ft.FilePicker(on_result=on_upload)
#     page.overlay.append(file_picker)
#
#     # --- TRANSCRIBE ---
#     def transcribe(e):
#         if not uploaded_file:
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
#             # Save uploaded bytes to temp file
#             with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
#                 f.write(uploaded_file.bytes)
#                 temp_path = f.name
#
#             with sr.AudioFile(temp_path) as source:
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
#     # --- COPY TEXT ---
#     def copy_text(e):
#         if transcription_text.value.strip():
#             page.set_clipboard(transcription_text.value)
#             status_text.value = "📋 Copied!"
#         else:
#             status_text.value = "Nothing to copy"
#
#         page.update()
#
#     # --- UI LAYOUT ---
#     page.add(
#         ft.Column(
#             [
#                 ft.Text("🎙 VocalScribe", size=30, weight="bold", color="white"),
#
#                 ft.Container(
#                     content=ft.Text("📁 Click here to upload audio file", color="black"),
#                     bgcolor="#d2b49c",
#                     padding=15,
#                     border_radius=30,
#                     alignment=ft.Alignment(0, 0),
#                     on_click=lambda _: file_picker.pick_files(allow_multiple=False),
#                     width=400
#                 ),
#
#                 transcription_text,
#
#                 ft.Row(
#                     [
#                         ft.ElevatedButton("Transcribe", on_click=transcribe),
#                         ft.ElevatedButton("Copy Text", on_click=copy_text),
#                     ],
#                     alignment=ft.MainAxisAlignment.CENTER
#                 ),
#
#                 status_text
#             ],
#             horizontal_alignment=ft.CrossAxisAlignment.CENTER
#         )
#     )
#
#
# if __name__ == "__main__":
#     port = int(os.environ.get("PORT", 8000))
#
#     ft.run(
#         main,                     # <-- main function as FIRST argument
#         view=ft.AppView.WEB_BROWSER,
#         port=port,
#         host="0.0.0.0"
#     )
#






#MAIN CODE WITH UNKNOWN FILEPICKER ERROR

# import flet as ft
# import speech_recognition as sr
# import os
#
# def main(page: ft.Page):
#     page.title = "VocalScribe"
#     page.bgcolor = "#4D0213"
#     page.padding = 20
#     page.vertical_alignment = ft.MainAxisAlignment.CENTER
#     page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
#
#     uploaded_file_path = None
#
#     # --- TEXT FIELD ---
#     transcription_text = ft.TextField(
#         hint_text="Audio Transcription",
#         multiline=True,
#         min_lines=5,
#         read_only=True,
#         width=500,
#         bgcolor="#3b3f45",
#         color="white",
#         border_radius=10
#     )
#
#     # --- STATUS ---
#     status_text = ft.Text("", color="white")
#
#     # --- LOADER ---
#     loader = ft.ProgressRing(visible=False)
#
#     # --- FILE PICKER ---
#     file_picker = ft.FilePicker()
#     page.overlay.append(file_picker)
#
#     def pick_file(e):
#         file_picker.pick_files(allow_multiple=False)
#
#     def on_file_selected(e):
#         nonlocal uploaded_file_path
#
#         if e.files:
#             uploaded_file_path = e.files[0].path
#             status_text.value = f"✅ Uploaded: {e.files[0].name}"
#         else:
#             status_text.value = "⚠️ No file selected"
#
#         page.update()
#
#     file_picker.on_result = on_file_selected
#
#     # --- TRANSCRIBE ---
#     def transcribe(e):
#         if not uploaded_file_path:
#             status_text.value = "Upload a file first!"
#             page.update()
#             return
#
#         loader.visible = True
#         status_text.value = "🎧 Transcribing..."
#         page.update()
#
#         try:
#             recognizer = sr.Recognizer()
#
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
#         loader.visible = False
#         page.update()
#
#     # --- DOWNLOAD ---
#     def download(e):
#         if not transcription_text.value.strip():
#             status_text.value = "Nothing to download"
#             page.update()
#             return
#
#         page.set_clipboard(transcription_text.value)
#         status_text.value = "📋 Copied to clipboard!"
#
#         page.update()
#
#     # --- UI ---
#     page.add(
#         ft.Column(
#             [
#                 ft.Text(
#                     "🎙 VocalScribe",
#                     size=32,
#                     weight="bold",
#                     color="#f5d6d6"
#                 ),
#
#                 ft.Container(
#                     content=ft.Text(
#                         "📁 Click here to upload audio file",
#                         color="black"
#                     ),
#                     bgcolor="#d2b49c",
#                     padding=18,
#                     border_radius=30,
#                     alignment=ft.Alignment(0, 0),
#                     on_click=pick_file,
#                     width=450
#                 ),
#
#                 transcription_text,
#
#                 loader,
#
#                 ft.Row(
#                     [
#                         ft.ElevatedButton(
#                             "📝 Transcribe",
#                             on_click=transcribe
#                         ),
#                         ft.ElevatedButton(
#                             "⬇ Download as .TXT",
#                             on_click=download
#                         ),
#                     ],
#                     alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
#                     width=500
#                 ),
#
#                 status_text
#             ],
#             horizontal_alignment=ft.CrossAxisAlignment.CENTER,
#             spacing=20
#         )
#     )
#
#
# if __name__ == "__main__":
#     port = int(os.environ.get("PORT", 8000))
#     ft.run(main, port=port)