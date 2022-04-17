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
       # obs = Popen(f'code {temp_dir} --user-data-dir {USER_DATA_DIR}', shell=True)
    if(mode==2):
        try:
            obs.kill()#TODO make this more graceful
        except:
            print("Exception: OBS is already closed.")

def loadAudio():
    global word_len_keys #These sounds can be used for whole words
    global single_keys
    fast_20_1 = AudioSegment.from_wav(r"./assets/typing_fast_20s.wav")
    single_1 = AudioSegment.from_wav(r"./assets/typing_single_1.wav")
    word_len_keys = [fast_20_1]
    single_keys = [single_1]

def randomAudio(mode):
    if(mode == 'single'):
        return single_keys[random.randint(0,len(single_keys)-1)]
    if(mode == 'word'):
        return word_len_keys[random.randint(0,len(word_len_keys)-1)]
    return None

async def start(proj_name, project_dir, pause, typo):
    global W, H
    W, H = pyautogui.size()
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
                await typeLines(lines, pause, typo)
            except UnicodeDecodeError:
                print(f"Skipping file: {i} . Presumably a non utf-8 file.") #TODO there is probably a better way to deal with these files
            time.sleep(random.randint(3, 10)/10)
            nanoSaveMacro()
    return

async def typeLines(lines, pause, typo):
    for line in lines:
        line = line.replace('\n', '')
        words = line.split(' ')
        for w in words: #Write word by word
            chance_pause_line = random.randint(1,20)
            chance_typo = random.randint(1,40)
            chance_pause_word = random.randint(1,60)
            try: 
                if chance_typo < typo: #Execute typo procedure
                    typo_w = randomlyChangeNChar(w, int(len(w)/5))#TODO 5 is arbitrary
                    playback = _play_with_simpleaudio(randomAudio('word'))
                    pyautogui.write(typo_w, interval=.05)
                    playback.stop()
                    time.sleep(random.randint(5, 15)/10)
                    for i in typo_w:
                        playback = _play_with_simpleaudio(randomAudio('single'))
                        pyautogui.press('backspace')
                        playback.stop()
                        #TODO add single key stroke sound here
            except Exception as e: print(e)
            if(w == '\t'):#Handle tabs, they need different sound and no space after.
                playback = _play_with_simpleaudio(randomAudio('single'))
                pyautogui.press('tab')
                playback.stop()
            playback = _play_with_simpleaudio(randomAudio('word'))
            pyautogui.write(w, interval=.0625)
            pyautogui.press('space')
            playback.stop()
            try:
                if chance_pause_word < pause:
                    time.sleep(random.randint(3, 15)/10)
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