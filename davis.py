import time
import rapidfuzz
import pyttsx3

from moonshine_voice import(
    MicTranscriber,
    TranscriptEventListener,
    get_model_for_language,
    download
)

model_path, model_arch = get_model_for_language("en", 5)

mic_transcriber = MicTranscriber(model_path=model_path, model_arch=model_arch,
update_interval=0.3, samplerate=50000)

class GoofyListener(TranscriptEventListener):

    def on_line_completed(self, event):
        print(event.line.text)


listener = GoofyListener()
mic_transcriber.add_listener(listener)
mic_transcriber.start()

while True:
    time.sleep(0.1)