**DAVIS -- Voice assistant for Helldivers 2**

Davis or, the 
**D**emocracy
**A**ssisted
**V**oice
**I**nput
**S**ystem

is a little quality of life program for Helldivers 2, written in Python. I am using Moonshine for voice recognition and (currently) pyttsx3 for text to speech. I intend on changning this to Piper or something later, but it'll do for now.
I fully intend on making this cross-compatible for Linux and Windows. Mac support is not feasible for me on my own, but if anyone wants to help out, I would appreciate it!
The idea is to make something COMPLETELY local, and easy on your system so it can run alongside the game.

Plan for first release
- Basic speech recognition capabilities
- Strategem support for ALL strategems, Warbond or not
- Options for using a push-to-talk or open mic for recognition
- Rebinding for keys
- Customizable wake word (default is Davis)
- A gui for easy configuration
- Multiple strategem callin with "and" keyword
- Text to speech with pyttsx3

Already done:
- Speech recognition
- Stratategem support for base + Redacted Regiment
- Customizable wake word

Future Stuff:
- Easy installation and use for the average user
- .exe and .tar.gz application stuff
- Custom trained model with the mooonshine fine-tune https://github.com/pierre-cheneau/finetune-moonshine-asr
- Voicelines based off of Pelican-1