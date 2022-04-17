#!/usr/bin/env python
import os, time
from subprocess import Popen
import argparse
import asyncio

from matplotlib.pyplot import pause
import sourcetyper

def parseArgs():
    arg_list = argparse.ArgumentParser()
    arg_list.add_argument("-d", "--dir", required=True,
        help="Directory of the target project")
    arg_list.add_argument("-p", "--pause", required=False,
        help="Enable random pasues during typing. Specify frequency from 1-10.")
    args = vars(arg_list.parse_args())
    dir = args['dir']
    pause = None
    try: pause = int(args['pause']) 
    except: print('Default pause off') 
    return dir, pause

async def main():
    dir, pause = parseArgs()
    lof = []
    if(not os.path.isdir(dir)):
        print(f'Error: {dir} is not a directory')
    for root, dirs, files in os.walk(dir):
        for file in files:
            lof.append(os.path.join(root,file))
    if(lof == []):
        print(f'Error: Target directory: {dir} is empty')
    project_name = sourcetyper.tmpDir(dir)

    sourcetyper.manageOBS(1) #Start OBS
    time.sleep(10)#TODO improve idk
    typer_task = asyncio.create_task( #Creates project files/folders and types code
        sourcetyper.start(project_name, dir, pause))
    await typer_task
    sourcetyper.closeGracefully()

    

if __name__ == '__main__':
    asyncio.run(main())