Needed markdown features:
    Create new file, folder
    Run program
    Run arbitrary terminal command
    Type code
    Pause statement
    Speed statement

Program Flow: (From terminal)
    Parse cmd line args
    Convert file structure to action list

    
Will create new project in a temporary folder by default

Type Speed: 16+ char/sec ?


Vscode command line interface features:
Extensions, file:line,
https://code.visualstudio.com/docs/editor/command-line

{
    "cmd","touch ./src/main.py",
    "keycombo":"ctrl+`", #This key combo will select the terminal
    "open:,"./api/endpoint.js",
    "text":"def parseFS(dir, main_file):\ndata = {}\nfor root, dirs, files in os.walk(dir):...."
}

keycombos:
ctrl+END Move cursor to end of file
ctrl+` Select the built in terminal

VScode Settings:
Session persistence: off
