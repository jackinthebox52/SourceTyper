#!/usr/bin/env python
import  os, shutil, time, random
import string
from subprocess import  Popen

from pydub import AudioSegment
from pydub.playback import _play_with_simpleaudio
import pyautogui

USER_DATA_DIR = '/tmp/sourcetyper/'

temp_dir = ''

def closeGracefully():
    manageOBS(2)#Stop OBS
    print('Closing')
    exit()

def tmpDir(dir):
    ndir = dir.split('/')
    ndir = ndir[len(ndir)-2]
    ndir = f'/tmp/{ndir}/'
    if(os.path.isdir(ndir)):
        shutil.rmtree(ndir)
    else:
        print(f'Initializing new project: {ndir}')
        global temp_dir
        temp_dir = ndir
        os.mkdir(f'{ndir}')
    return ndir #Return project name

def manageOBS(mode):
    global obs
    if(mode==1):
        obs = Popen(['obs', '--startrecording', '--minimize-to-tray', '--scene', 'SourceTyper'])
    if(mode==2):
        try:    obs.kill()#TODO make this more graceful
        except:     print("Exception: OBS is already closed.")

def loadAudio():
    audio_dir = './assets/audio/'
    global word_keys #These sounds can be used for whole words
    global single_keys
    word_keys = {}
    single_keys = {}
    for f in os.listdir(f'{audio_dir}typing_word'):
        if '.wav' in f:
            name = f.split('.')[0]
            auds = AudioSegment.from_wav(f'{audio_dir}typing_word/{f}')
            word_keys[name] = auds
            print(f'Loaded audio file: {audio_dir}typing_word/{f}')
    for f in os.listdir(f'{audio_dir}typing_single'):
        if '.wav' in f:
            name = f.split('.')[0]
            auds = AudioSegment.from_wav(f'{audio_dir}typing_single/{f}')
            single_keys[name] = auds
            print(f'Loaded audio file: {audio_dir}typing_single/{f}')
    #fast_20_1 = AudioSegment.from_wav(r"./assets/typing_fast_20s.wav")
    #single_1 = AudioSegment.from_wav(r"./assets/typing_single_1.wav")
    #word_keys = [fast_20_1]
    #single_keys = [single_1]

def randomAudio(mode):
    if(mode == 'single'):
        index, sound = random.choice(list(single_keys.items()))
        print(f'Playing single stroke audio: {index}.wav')
        return sound
    if(mode == 'word'):
        index, sound = random.choice(list(word_keys.items()))
        #print(f'Playing word audio: {index}.wav')
        return sound
    return None

async def start(proj_name, project_dir, pause, typo, s):
    loadAudio()
    execCommand(f'cd {proj_name}')
    for root, dirs, files in os.walk(project_dir):
        for i in files:
            if(i == '.stignore'):
                pass
            local_dir = './' + root.replace(project_dir, '')
            local_file = local_dir + f'/{i}' #TODO fix double slash on some local files
            if(not os.path.isdir(local_dir)):
                execCommand(f'mkdir -p {local_dir}')
            execCommand(f'nano {local_file}')
            l = open(os.path.join(root, i), 'r')
            try:
                lines = l.readlines()
                await typeLines(lines, pause, typo, s)
            except UnicodeDecodeError:
                print(f"Skipping file: {i} . Presumably a non utf-8 file.") #TODO there is probably a better way to deal with these files
            time.sleep(random.randint(3, 10)/10)
            nanoSaveMacro()
    return

async def typeLines(lines, pause, typo, s):
    global speed
    global base_speed
    if(s == None):
        speed = 0.0625 #Default speed of 16 char/s
    else:
        base_speed = 1 / s                                                                   #Convert char/sec to decimal wait interval
        speed = base_speed  
    for line in lines:
        line = line.replace('\n', '')
        words = line.split(' ')
        for w in words: #Write to terminal word by word #Unindent this block
            chance_pause_line = random.randint(1,20)#Needs work
            chance_typo = random.randint(1,60)
            chance_pause_word = random.randint(1,60)#Needs work
            chance_change_speed = random.randint(1,3)#Needs work
            if(chance_change_speed == 2):
                speed = random.uniform(speed * .85, speed * 1.15)
                #print(f'Speed varied to:{speed} char')
            try: 
                if chance_typo < typo:                                                  #Execute typo procedure
                    typo_w = randomlyChangeNChar(w, int(len(w)/6))#TODO 6 is arbitrary
                    playback = _play_with_simpleaudio(randomAudio('word'))
                    pyautogui.write(typo_w, interval=speed)
                    playback.stop()
                    time.sleep(random.randint(0, 5)/10)
                    for i in typo_w:
                        playback = _play_with_simpleaudio(randomAudio('single'))
                        pyautogui.press('backspace')
                        playback.stop()
                        #TODO add single key stroke sound here
            except TypeError as e: pass #TODO catch other errors
            if(w == ' '):                                                  #Handle tabs, they need different sound and no space after.
                print('TAB!')
                playback = _play_with_simpleaudio(randomAudio('single'))
                pyautogui.press('tab')
            else:
                playback = _play_with_simpleaudio(randomAudio('word'))
                pyautogui.write(w, interval=speed)
                pyautogui.press('space')
                playback.stop()
            try:
                if chance_pause_word < pause:
                    time.sleep(random.randint(3, 9)/10)
            except: pass
        pyautogui.press('enter')
        try:
            if chance_pause_line < pause:
                time.sleep(random.randint(10, 30)/10)
        except: pass
    time.sleep(random.randint(3, 10)/10)
    return

# Method to change N characters from a string with random characters.
def randomlyChangeNChar(word, value):
    length = len(word)
    word = list(word)
    # This will select the two distinct index for us to replace
    k = random.sample(range(0,length),value)
    for index in k:
        # This will replace the characters at the specified index with 
        # the generated characters
        word[index] = random.choice(string.ascii_lowercase + " ")
    # Finally print the string in the modified format.
    return("" . join(word))

def execCommand(cmd):
    playback = _play_with_simpleaudio(randomAudio('word'))
    pyautogui.write(cmd, interval=.0625)
    pyautogui.press('enter')
    playback.stop()
    time.sleep(random.randint(3, 10)/10)
    return

def nanoSaveMacro():
    pyautogui.hotkey('ctrl', 'x')
    time.sleep(random.randint(3, 10)/10)
    pyautogui.press('y')
    time.sleep(random.randint(3, 10)/10)
    pyautogui.press('enter')
    time.sleep(random.randint(3, 10)/10)
    return