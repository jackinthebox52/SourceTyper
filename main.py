#!/usr/bin/env python
import os, time
from subprocess import Popen
import argparse
import asyncio

from matplotlib.pyplot import pause
import typer

def closeGracefully():
    typer.manageOBS(2)#Stop OBS
    print('Closing')
    exit()

def parseArgs():
    arg_list = argparse.ArgumentParser()
    arg_list.add_argument("-d", "--dir", required=True,
        help="Directory of the target project")
    arg_list.add_argument("-p", "--pause", required=False,
        help="Enable random pasues during typing. Specify frequency from 1-10")
    arg_list.add_argument("-t", "--typo", required=False,
        help="Enable random typos. Specify frequency from 1-10")
    arg_list.add_argument("-s", "--speed", required=False,
        help="Specify average typing speed in char/sec. Default = 16char/sec = 480word/min")
    args = vars(arg_list.parse_args())
    dir = args['dir']
    pause = None
    try: pause = int(args['pause']) 
    except: print('Default pause off') 
    typo = None
    try: typo = int(args['typo']) 
    except: print('Default typo off') 
    speed = None
    try: speed = int(args['speed']) 
    except: print('Default speed 16char/sec') 

    return dir, pause, typo, speed

async def main():
    dir, pause, typo, speed = parseArgs()
    lof = []
    if(not os.path.isdir(dir)):
        print(f'Error: {dir} is not a directory')
    for root, dirs, files in os.walk(dir):
        for file in files:
            lof.append(os.path.join(root,file))
    if(lof == []):
        print(f'Error: Target directory: {dir} is empty')
    project_name = typer.tmpDir(dir)

    typer.manageOBS(1) #Start OBS
    time.sleep(10)#TODO improve idk
    typer_task = asyncio.create_task( #Creates project files/folders and types code
        typer.start(project_name, dir, pause, typo, speed))
    await typer_task
    closeGracefully()

if __name__ == '__main__':
    asyncio.run(main())