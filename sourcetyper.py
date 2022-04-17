#!/usr/bin/env python
import  os, shutil, time, random
from subprocess import  Popen

from pydub import AudioSegment
from pydub.playback import _play_with_simpleaudio
import pyautogui
from pathlib import Path

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
    global type_sound
    #pydub.AudioSegment.converter = os.path.dirname(os.path.abspath(__file__)) + r"\ffmpeg.exe"
    typing20 = AudioSegment.from_wav(r"./assets/typing20.wav")
    type_sound = typing20

async def start(proj_name, project_dir, pause):
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
            hard_dir = f'/tmp/{proj_name}/' + root.replace(project_dir, '')
            hard_file = os.path.join(hard_dir, i)
            if(not os.path.isdir(local_dir)):
                execCommand(f'mkdir -p {local_dir}')
            execCommand(f'nano {local_file}')
            l = open(os.path.join(root, i), 'r')
            try:
                lines = l.readlines()
                await typeLines(lines, pause)
            except UnicodeDecodeError:
                print(f"Skipping file: {i} . Presumably a non utf-8 file.") #TODO there is probably a better way to deal with these files
            time.sleep(random.randint(3, 10)/10)
            pyautogui.hotkey('ctrl', 'x')
            time.sleep(random.randint(3, 10)/10)
            pyautogui.press('y')
            time.sleep(random.randint(3, 10)/10)
            pyautogui.press('enter')
            time.sleep(random.randint(3, 10)/10)
    return

async def typeLines(lines, pause):
    pause_freq = pause #TODO base the amount of time to pause for on the speed that we are typing at
    if not pause == None: pause = True
    else: pause = False
    for line in lines:
        line = line.replace('\n', '')
        words = line.split(' ')
        c1 = random.randint(1,20)
        for w in words: #Write word by word
            c2 = random.randint(1,50)
            playback = _play_with_simpleaudio(type_sound)
            pyautogui.write(w, interval=.0625)
            pyautogui.press('space')
            playback.stop()
            if c2 < pause_freq:
                time.sleep(random.randint(3, 10)/10)
        pyautogui.press('enter')
        if c1 < pause_freq:
            time.sleep(random.randint(10, 30)/10)
            
    time.sleep(random.randint(3, 10)/10)
    return

def execCommand(cmd):
    playback = _play_with_simpleaudio(type_sound)
    pyautogui.write(cmd, interval=.0625)
    pyautogui.press('enter')
    playback.stop()
    time.sleep(random.randint(3, 10)/10)
    return
