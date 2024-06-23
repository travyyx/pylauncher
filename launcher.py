import os
from datetime import date
import json
from pathlib import Path
import typer
from pydantic import BaseModel

today = date.today()

class App(BaseModel):
    name: str
    desc: str
    creationDate: date = today
    command: str
    path: str

app = typer.Typer()

class Launcher:
    def __init__(self):
        self.cwd = os.getcwd()
        self.DIR_NAME: str = "pylauncher"
        self.APPS_DIR: str = "apps"
        self.PATH: str = os.path.join(self.cwd, self.DIR_NAME)
        self.APPS_PATH: str = os.path.join(self.PATH, self.APPS_DIR)
        self.today = date.today()
        self.commands = ["Add program", "Run Program", "List Programs", "Edit Program", "Remove Program", "Help", "Reset Launcher", "About"]

        if not os.path.exists(self.PATH):
            os.makedirs(self.PATH)
            os.makedirs(self.APPS_PATH)
            f = open(os.path.join(self.PATH, "apps.json"), "w+", encoding='utf-8')
            f.write(json.dumps({ "apps": {}, "version": 1.0}, indent=4))
            f.close()

        self.appdata = json.loads(open(os.path.join(self.PATH, "apps.json"), 'r+', encoding='utf-8').read())
        
    
    def start(self):

        self.clear()
        with open(os.path.join(self.PATH, "apps.json"), 'r', encoding='utf-8') as f:
            self.appdata = json.loads(f.read())

        print("----------- Python App Launcher -----------------")
        print(f"------- Version {self.appdata['version']}, Travislicious --------------")
        print("")

        i = 1
        for command in self.commands:
            print(f"{i}> {command}")
            i += 1
        
        print(f"\n------- Today Date: {self.today} ----------------------")
        
        choice = input("Choose one option: ")

        if choice and choice.isdigit():
            if int(choice) == 1:
                self.add_program()
            elif int(choice) == 2:
                self.run_program()
            elif int(choice) == 3:
                self.list_program()
            elif int(choice) == 4:
                self.edit_program()
            elif int(choice) == 5:
                self.remove_program()
            elif int(choice) == 6:
                self.print_help()
            elif int(choice) == 7:
                self.reset_launcher()
            elif int(choice) == 8:
                self.print_about()
            else:
                print("This command doesn't exists, try again")
                quit()
        else:
            print("Command error.")
            quit()
            
    
    def add_program(self):

        self.clear()
        print("--------------------------- Add Program ------------------------")
        progname = input("Program Name: ")

        if progname in self.appdata["apps"].keys():
            print("This program already exists.")
            quit()
        
        progpath = input("Program Path: ")

        if not os.path.isfile(progpath) and progpath.endswith(".py"):
            print("the program doesn't exists.")
            quit()
        
        progdesc = input("[Optional] Program Description (max 20 letters): ")

        if progdesc and int(progdesc >= 20):
            print("The description is too long.")
            quit()
        
        progcommand = input("Program Command name: ")

        if progname and progcommand and progpath:
            new_app = App(name=progname, desc=progdesc if progdesc else "A simple program.", command=progcommand, path=progpath)
            json_data = new_app.model_dump_json(indent=4)
            filename = Path(os.path.join(self.APPS_PATH, f"{progname}.json"))
            filename.touch(exist_ok=True)

            with open(filename, "w+", encoding="utf-8") as f:
                f.write(json_data)
                f.close()

            self.appdata["apps"][progname] = progpath
            with open(os.path.join(self.PATH, "apps.json"), 'w+', encoding='utf-8') as f:
                f.write(json.dumps(self.appdata, indent=4))
                f.close()

            print("----------------- App Added successfully. ------------------")
            self.start()


    
    def list_program(self):
        self.clear()

        if len(self.appdata["apps"]) == 0:
            print("No programs added yet.")
            quit()
        else:
            i = 1
            print(f'--------------------------- Programs: {len(self.appdata["apps"])} ----------------------\n')
            for name, path in self.appdata["apps"].items():
                    print(f"[{i}] {name} > {path}")
                
                    i += 1
            
            back = input("[Enter] Go Back.\n")

            if back == "":
                self.start()
                
    
    def edit_program(self):
        self.clear()
        if len(self.appdata["apps"]) == 0:
            print("No programs added yet.")
            quit()
        else:
            i = 1
            print(f'--------------------------- Choose Program: {len(self.appdata["apps"])} ----------------------\n')
            for name, path in self.appdata["apps"].items():
                    print(f"[{i}] {name} > {path}")
                
                    i += 1
            
            progname = input("Enter Program Name: ")

            if progname not in self.appdata["apps"].keys():
                print("This program doesn't exists.")
                quit()

            if progname in self.appdata["apps"].keys():
                self.clear()
                print("------------------------ Edit Program --------------------------")
                progdesc = input("[Optional] Program Description: ")
                progcommand = input("Program Command: ")
                progpath = input("Program Path: ")

                if progdesc and int(progdesc) >= 20:
                    print("The description is too long.")
                    quit()
                
                if not os.path.isfile(progpath) and progpath.endswith(".py"):
                    print("the program doesn't exists.")
                    quit()

                self.appdata["apps"][progname] = progpath
                if progcommand and progpath:
                    with open(os.path.join(self.PATH, "apps.json"), 'w+', encoding='utf-8') as f:
                        f.write(json.dumps(self.appdata, indent=4))
                        f.close()

                    new_app = App(name=progname, desc=progdesc if progdesc else "A simple program.", command=progcommand, path=progpath)
                    json_data = new_app.model_dump_json(indent=4)
                    filename = Path(os.path.join(self.APPS_PATH, f"{progname}.json"))
                    with open(filename, 'w+', encoding='utf-8') as f:
                        f.write(json_data)
                        f.close()

                    print("----------------- Program Edited ----------------")
            
    
    def print_help(self):
        self.clear()
        print("To use the launcher, you can go to the menu and select and option. or you can just use the cli to do something. 1: Add a program to the launcher, 2: Run an added program, 3: list all of the added programs, 4: edit a program, 5: remove a program. \n")

        back = input("[Enter] Go Back.\n")

        if back == "":
            self.start()
    
    def print_about(self):
        self.clear()
        print("--------------------------- Python Program Launcher --------------------------")
        print("Copyright 2024, Travislicious.\n")

        back = input("[Enter] Go Back.\n")

        if back == "":
            self.start()
    
    def remove_program(self):
        self.clear()
        if len(self.appdata["apps"]) == 0:
            print("No programs added yet.")
            quit()
        else:
            i = 1
            print(f'--------------------------- Choose Program: {len(self.appdata["apps"])} ----------------------\n')
            for name, path in self.appdata["apps"].items():
                    print(f"[{i}] {name} > {path}")
                
                    i += 1
            
            progname = input("Enter Program Name: ")

            if progname not in self.appdata["apps"].keys():
                print("This program doesn't exists.")
                quit()

            if progname:
                self.clear()
                print("-------------------- Remove Program -----------------------")

                choice = input(f"[{progname}] Are you sure to delete this program (Y/n): ")

                if choice == "Y" or "y":
                    filename = Path(os.path.join(self.APPS_PATH, f"{progname}.json"))
                    del self.appdata["apps"][progname]
                    with open(os.path.join(self.PATH, "apps.json"), 'w+', encoding='utf-8') as f:
                        f.write(json.dumps(self.appdata, indent=4))
                        f.close()
                    
                    os.remove(filename)

                    print("------------------ Program Deleted -----------------------------")
                
                elif choice == "N" or "n":
                    self.start()

                else:
                    print("Invalid choice.")
                    quit()
    
    def reset_launcher(self):
        self.clear()
        
        choice = input("Are you sure to reset the launcher. All datas will be erased. (Y/n): ")

        if choice == "Y" or "y":
            os.remove(os.path.join(self.PATH, "apps.json"))
            os.rmdir(self.APPS_PATH)
            os.rmdir(self.PATH)

            print("----------------------------- Launcher Cleaned ------------------------")
        elif choice == "N" or "n":
            self.start()
    
    def run_program(self):
        self.clear()
        if len(self.appdata["apps"]) == 0:
            print("No programs added yet.")
            quit()
        else:
            i = 1
            print(f'--------------------------- Choose Program: {len(self.appdata["apps"])} ----------------------\n')
            for name, path in self.appdata["apps"].items():
                    print(f"[{i}] {name} > {path}")
                
                    i += 1
            
            progname = input("Enter Program Name: ")

            if progname not in self.appdata["apps"].keys():
                print("This program doesn't exists.")
                quit()

            if progname:
                progpath = self.appdata["apps"][progname]
                self.clear()
                os.system(f"python {progpath}" if os.name == 'nt' else f"python3 {progpath}")
    
    def clear(self):

        os.system('cls' if os.name == 'nt' else 'clear')

    
    def run(self, name: str):
        """ Run a program using its name."""

        if len(self.appdata["apps"]) == 0:
            print("No programs added yet.")
            quit()
        else:
            if name not in self.appdata["apps"].keys():
                print("This program doesn't exists.")
                quit()

            if name:
                progpath = self.appdata["apps"][name]
                self.clear()
                os.system(f"python {progpath}" if os.name == 'nt' else f"python3 {progpath}")


@app.command("run")
def run_cli(name: str):
    """ Run a program using its name."""
    launcher = Launcher()
    launcher.run(name)

@app.command("init")
def init_cli():
    """ Init the app."""
    launcher = Launcher()
    launcher.start()

@app.command("list")
def list_progs():
    """ List added programs"""
    launcher = Launcher()
    launcher.list_program()

@app.command("about")
def about():
    """ Give information about the app."""
    launcher = Launcher()
    launcher.print_about()

@app.command("reset")
def reset():
    """ Reset the app."""
    launcher = Launcher()
    launcher.reset_launcher()

app()
