import time
import rapidfuzz
import pyautogui
import mouse
import threading
import subprocess
import queue
import pyttsx3
import keyboard

from moonshine_voice import(
    MicTranscriber,
    TranscriptEventListener,
    get_model_for_language,
    download,
    transcriber
)

tts = pyttsx3.init()
tts.setProperty('volume', 0.3)

callins = {
    # Patriotic Administration Center
    'eat': 'ddlur',
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
    'eagle 500': 'urddd',
    'fast recon vehicle': 'ldrdrdu',
    'supply truck': 'ldlldur',

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
    'bullet dog': 'dulurd',
    'autocannon sentry': 'durulu',
    'rocket sentry': 'durrl',
    'ems mortar': 'durdr',
    'mortar sentry': 'durdr',
    'patriot': 'ldruldd',
    'emancipator': 'ldruldu',
    'bastion': 'ldrdldudu',

    # Python Commandos
    'hot dog': 'dulull',
    'chainsaw': 'dlrrd',
    'maxigun': 'dlrduu',


    # Redacted Regiment
    'c4 pack': 'druuru',

    # Entrenched Division
    'cremator': 'ddrduu',
    'gas mortar': 'durdl',

    # Exo Experts
    'bullet storm': 'dldrul',
    'breakthrough': 'ldrlrdu',
    'lumberer': 'ldrurlu',

    # Common
    'reinforce': 'udrlu',
    'sos': 'udru',
    'resupply': 'ddur',
   # 'eagle rearm': 'uulur',

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
    'one twenty': '120',
    'three eighty': '380',
    'five hundred': '500',
    'four': '4',
    ' strike': '',
    'over the': 'orbital',
    'over to': 'orbital',
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



pyautogui.PAUSE=0.05
pyautogui.FAILSAFE=False
def enter_stratagem():

    while True:
        formatted_txt = strat_queue.get()
        strategem = rapidfuzz.process.extract(query=formatted_txt, 
                                            choices=callins.keys(), 
                                            scorer=rapidfuzz.fuzz.WRatio, 
                                            score_cutoff=51,
                                            processor=rapidfuzz.utils.default_process)
        
        print(strategem)

        if strategem != []:
            tts_queue.put('Right away sir')
            strategem = strategem[0][0]
            print(f'Detected: {strategem}')


            print('Waiting for strategem key down or mouse up')
        
            # Strategem key is not held or the mouse is down
            while not strat_down.is_set() or mouse_down.is_set():
                time.sleep(0.1)

            for i in callins[strategem]:
                pyautogui.keyDown(control_dict[i])
                pyautogui.keyUp(control_dict[i])
            
            print(f'Entered strategem: {strategem}')


            print('Waiting for mouse down...')
            # Wait for a mouse down to throw or strategem key release
            
            while strat_down.is_set() and not mouse_down.is_set():
                time.sleep(0.1)   

            print('Waiting for mouse up...')
            # Wait for a mouse up to finish throw or strategem key release
            while strat_down.is_set() and mouse_down.is_set():
                time.sleep(0.1)

            print('Finished')     

            mic_transcriber.stop()
            time.sleep(0.25)
            mic_transcriber.start()

        else:
            print('No strategem detected...')


def format(txt):
    txt = txt.strip().lower()

    for key in replace_dict.keys():
        if key in txt:
            txt = txt.replace(key, replace_dict[key])

    return txt.strip()


# model_path, model_arch = get_model_for_language("en", 2)
model_path, model_arch = get_model_for_language("en", 5)

mic_transcriber = MicTranscriber(
    model_path=model_path,
    model_arch=model_arch,
    update_interval=0.7,       
    options={
        "vad_window_duration": "0.25",      
        "vad_max_segment_duration": "5",  
        "transcription_interval": "0.2",     
        "vad_threshold": "0.5",             
    })

class GoofyListener(TranscriptEventListener):

    # def on_line_started(self, event):
    #     print(event.line.text)

    def on_line_completed(self, event):
        if strat_down.is_set(): # Janky PTT, bound to same key as stratagem input
            raw_txt = format(event.line.text)
            print(raw_txt)
            process_queue.put(raw_txt)
        

def tts_mainloop():
    while True:
        tts.say(tts_queue.get())
        tts.runAndWait()


def process_mainloop():

    while True:

        raw_txt = process_queue.get()
        # Add wake word fuzz!
        # wake_txt = rapidfuzz.process.extractOne(query='davis', 
        #                                 choices=raw_txt.split(' '), 
        #                                 scorer=rapidfuzz.fuzz.ratio, 
        #                                 score_cutoff=70)
        wake_txt = rapidfuzz.fuzz.partial_ratio_alignment('davis', raw_txt, score_cutoff=70)

        print(wake_txt)
        print(raw_txt)

        if wake_txt is not None:
            try:

                print('Activated!')

                # raw_txt = raw_txt.replace(wake_txt.dest_end, 'davis')
                # raw_txt = 'davis' + raw_txt[wake_txt.dest_end:]
                # print(raw_txt)
                formatted_txt = raw_txt[wake_txt.dest_end:].strip()
                print(formatted_txt)
                if 'and' in formatted_txt:
                    commands = formatted_txt.split('and')

                    for command in commands:

                        strat_queue.put(command)

                else:
                    strat_queue.put(formatted_txt)

            except Exception as e:
                print(e)

TRANSCRIBER_RESET_INTERVAL = 120  # seconds

def transcriber_reset_loop():
    while True:
        time.sleep(TRANSCRIBER_RESET_INTERVAL)
        print("Resetting transcriber...")
        tts_queue.put('Reset')
        mic_transcriber.stop()
        time.sleep(1)
        mic_transcriber.start()
        print("Transcriber reset.")
        tts_queue.put('Back in the fight, sir!')



print('Listening...')
listener = GoofyListener()
mic_transcriber.add_listener(listener)
mic_transcriber.start()

#print(subprocess.run("for i in $(pgrep python); do sudo renice -n -20 -p $i; done", shell=True, capture_output=True))

mouse_down = threading.Event()
strat_down = threading.Event()


tts_queue = queue.Queue()
tts_thread = threading.Thread(daemon=True, target=tts_mainloop)
tts_thread.start()
tts_queue.put('Ready to support democracy with you, sir')


strat_queue = queue.Queue()
strat_thread = threading.Thread(daemon=True, target=enter_stratagem)
strat_thread.start()
print('strat thread')
process_queue = queue.Queue()
process_thread = threading.Thread(daemon=True, target=process_mainloop)
process_thread.start()

print('process thread')

# reset_thread = threading.Thread(daemon=True, target=transcriber_reset_loop)
# reset_thread.start()


while True:

    if mouse.is_pressed("left"):
        mouse_down.set()

    else:
        mouse_down.clear()

    # if mouse.is_pressed('x2'):
    if keyboard.is_pressed('capslock'):  
        strat_down.set()
        
    else:
        strat_down.clear()

    time.sleep(0.1)