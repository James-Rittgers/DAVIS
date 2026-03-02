import time
import rapidfuzz
import pyttsx3
import pyautogui

from moonshine_voice import(
    MicTranscriber,
    TranscriptEventListener,
    get_model_for_language,
    download
)

wake_word = 'davis'

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
            '.': '',
            ',': '',
            '?': '',
            '!': '',
            ';': '',
            ':': ''
}

pyautogui.PAUSE=0.01
pyautogui.FAILSAFE=False
def enter_strategem(strategem):
    for i in callins[strategem]:
        pyautogui.keyDown(control_dict[i])
        pyautogui.keyUp(control_dict[i])

def format(txt):
    txt = txt.strip().lower()

    for key in replace_dict.keys():
        if key in txt:
            txt = txt.replace(key, replace_dict[key])

    return txt.strip()

model_path, model_arch = get_model_for_language("en", 5)

mic_transcriber = MicTranscriber(model_path=model_path, model_arch=model_arch,
update_interval=0.1, samplerate=16000)

class GoofyListener(TranscriptEventListener):

    def on_line_completed(self, event):
        text_in = format(event.line.text)
        print(text_in)

        if wake_word in text_in:
            print('Activated!')
            command = text_in.split('davis')[1].strip()

            strategem = rapidfuzz.process.extract(query=command, choices=callins.keys(), scorer=rapidfuzz.fuzz.QRatio, score_cutoff=50)
            
            if strategem != []:
                strategem = strategem[0][0]
                print(f'Detected: {strategem}')
                enter_strategem(strategem)

            else:
                print('No strategem detected...')

print('Listening...')
listener = GoofyListener()
mic_transcriber.add_listener(listener)
mic_transcriber.start()

while True:
    time.sleep(0.01)