import time
import rapidfuzz
import pyttsx3
import pyautogui
import mouse
import subprocess

from moonshine_voice import(
    MicTranscriber,
    TranscriptEventListener,
    get_model_for_language,
    download,
    transcriber
)
from james_transcriber import JamesTranscriber

tts = pyttsx3.init()

callins = {
    # Patriotic Administration Center
    'expendable anti-tank': 'ddlur',
    'machine gun': 'dldur',
    'anti-material rifle': 'dlrud',
    'stalwart': 'dlduul',
    'recoilless rifle': 'dlrrl',
    'flamethrower': 'dludu',
    'autocannon': 'dlduur',
    'heavy machine gun': 'dludd',
    'airburst rocket launcher': 'duulr',
    'commando': 'dludr',
    'railgun': 'drdulr',
    'spear': 'ddudd',
    'wasp': 'ddudr',

    # Orbital Cannons
    'orbital gatling': 'rdluu',
    'orbital airburst': 'rrr',
    'orbital 120': 'rrdlrd',
    'orbital 380': 'rduuldd',
    'orbital walking': 'rdrdrd',
    'orbital laser': 'rdurd',
    'orbital napalm': 'rrdlru',
    'orbital railcannon': 'ruddr',

    # Hangar
    'eagle strafe': 'urr',
    'eagle airstrike': 'urdr',
    'eagle cluster': 'urddr',
    'eagle napalm': 'urdu',
    'jump pack': 'duudu',
    'eagle smoke': 'urud',
    'eagle rocket pods': 'urul',
    'eagle 500 kg': 'urddd',
    'fast recon vehicle': 'ldrdrdu',

    # Bridge
    'orbital precision': 'rru',
    'orbital gas': 'rrdr',
    'orbital ems': 'rrld',
    'orbital smoke': 'rrdu',
    'hmg emplacement': 'dulrrl',
    'shield generator': 'ddlrlr',
    'tesla tower': 'durulr',
    'grenadier battlement': 'drdlr',

    # Engineering Bay
    'anti-personnel mine': 'dlur',
    'supply pack': 'dlduud',
    'grenade launcher': 'dluld',
    'laser cannon': 'dldul',
    'incendiary mine': 'dlld',
    'laser dog': 'dulurr',
    'ballistic shield': 'dlddul',
    'arc thrower': 'drdull',
    'anti-tank mine': 'dluu',
    'quasar cannon': 'ddulr',
    'shield generator backpack': 'dulrlr',
    'gas mine': 'dllr',
    
    # Robotics workshop
    'machine gun sentry': 'durru',
    'gatling sentry': 'durl',
    'mortar sentry': 'durrd',
    'bullet dog': 'dulurd',
    'autocannon sentry': 'durulu',
    'rocket sentry': 'durrl',
    'ems mortar': 'durdr',
    'mortar': 'durdr',
    'patriot': 'ldruldd',
    'emancipator': 'ldruldu',
    'bastion': 'ldrdldudu',


    # Redacted Regiment
    'c4 pack': 'druuru',

    # Common
    'reinforce': 'udrlu',
    'sos': 'udru',
    'resupply': 'ddur',
    'eagle rearm': 'uulur',

    #Objectives
    'sssd': 'ddduu',
    'prospecting drill': 'ddlrdd',
    'super earth flag': 'dudu',
    'hell bomb': 'duldurdu',
    'upload data': 'lruuu',
    'seismic probe': 'uulrdd',

    # Other
    's e a f artillery': 'ruud',
    'super destroyer': 'uuddlrlr'       
}

control_dict = {
    'd': 'down',
    'u': 'up',
    'l': 'left',
    'r': 'right'
}

replace_dict = {
    'barrage': '',
    'air strike': 'airstrike',
    ' strike': '',
    'orbitel': 'orbital',
    'orville': 'orbital',
    'century': 'sentry',
    'auto cannon': 'autocannon',
    'relay': '',
    'mines': 'mine',
    'minefield': 'mine',
    'ark': 'arc',
    'thriller': 'thrower',
    'rail cannon': 'railcannon',
    'fast recon': 'fast recon vehicle',
    'recoilest': 'recoilless',
    'hellbomb': 'hell bomb',
    'air ': 'airburst',
    '.': '',
    ',': '',
    '?': '',
    '!': '',
    ';': '',
    ':': ''
}

tts.say('Ready to support democracy with you, sir')
tts.runAndWait()
tts.say('Power cycle your headset')
tts.runAndWait()

pyautogui.PAUSE=0.03
pyautogui.FAILSAFE=False
def enter_strategem(formatted_txt):
    global strat_down, mouse_down

    strategem = rapidfuzz.process.extract(query=formatted_txt, 
                                        choices=callins.keys(), 
                                        scorer=rapidfuzz.fuzz.QRatio, 
                                        score_cutoff=50)
    
    if strategem != []:
        strategem = strategem[0][0]
        print(f'Detected: {strategem}')

        # tts.say('Waiting for keydown')
        # tts.runAndWait()
        print('Waiting for strategem key down or mouse up')
    
        # Strategem key is not held or the mouse is down
        while strat_down == False or mouse_down == True:
            time.sleep(0.01)

        for i in callins[strategem]:
            pyautogui.keyDown(control_dict[i])
            pyautogui.keyUp(control_dict[i])
        
        print(f'Entered strategem: {strategem}')
        # tts.say('Entered strategem')
        # tts.runAndWait()

        print('Waiting for mouse down...')
        # Wait for a mouse down to throw or strategem key release
        while mouse_down == False and strat_down == True:
            time.sleep(0.01)   

        print('Waiting for mouse up...')
        # Wait for a mouse up to finish throw or strategem key release
        while mouse_down == True and strat_down == True:
            time.sleep(0.01)

        print('Finished')     

    else:
        print('No strategem detected...')


def format(txt):
    txt = txt.strip().lower()

    for key in replace_dict.keys():
        if key in txt:
            txt = txt.replace(key, replace_dict[key])

    return txt.strip()


model_path, model_arch = get_model_for_language("en", 2)

mic_transcriber = JamesTranscriber(model_path=model_path, model_arch=model_arch,
                                update_interval=0.7, samplerate=16000, m_options={"vad_window_duration": "0.5",
                                                                                "vad_max_segment_duration": "15", 
                                                                                "transcription_interval": "0.05"})

class GoofyListener(TranscriptEventListener):

    # def on_line_started(self, event):
    #     print(event.line.text)

    def on_line_completed(self, event):
        global mouse_down
        raw_txt = format(event.line.text)
        print(raw_txt)

        # Add wake word fuzz!
        if 'davis' in raw_txt:
            print('Activated!')
            tts.say('Right away sir')
            tts.runAndWait()

            formatted_txt = raw_txt.split('davis')[1].strip()
            print(formatted_txt)
            if 'and' in formatted_txt:
                commands = formatted_txt.split('and')
                # tts.say(f'multiple commands detected')
                # tts.runAndWait()

                for command in commands:
                    # tts.say(f'Command {commands.index(command) +1}')
                    # tts.runAndWait()
                    enter_strategem(command)

            else:
                enter_strategem(formatted_txt)

print('Listening...')
listener = GoofyListener()
mic_transcriber.add_listener(listener)
mic_transcriber.start()

print(subprocess.run("for i in $(pgrep python); do sudo renice -n -20 -p $i; done", shell=True, capture_output=True))

while True:
    mouse_down = mouse.is_pressed("left")
    strat_down = mouse.is_pressed('x2')
