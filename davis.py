from moonshine_voice import *

transcriber = Transcriber(model_path=model_path, model_arch=model_arch)

class TestListener(TranscriptEventListener):
    def on_line_started(self, event):
        print(f"Line started: {event.line.text}")

    def on_line_text_changed(self, event):
        print(f"Line text changed: {event.line.text}")

    def on_line_completed(self, event):
        print(f"Line completed: {event.line.text}")

   
transcriber.add_listener(listener)


audio_data, sample_rate = load_wav_file(wav_path)

transcriber.start()

# Loop through the audio data in chunks to simulate live streaming
# from a microphone or other source.
chunk_duration = 0.1
chunk_size = int(chunk_duration * sample_rate)
for i in range(0, len(audio_data), chunk_size):
    chunk = audio_data[i: i + chunk_size]
    transcriber.add_audio(chunk, sample_rate)

transcriber.stop()

