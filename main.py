# -*- coding: utf-8 -*-
# author: Madhav (https://github.com/madhav-mknc)

from os import system as cmd
from waitress import serve
from configs import HOST, PORT

# run app.py
def main():
    print("[booting...]")
    
    from app import app
    
    print("[GOING ONLINE...]")
    serve(app, host=HOST, port=PORT)


# install dependencies
def install(err):
    print("[error]",err)
    print("[*] Installing the Requirements")
    
    with open('requirements.txt', 'r') as file:
        reqs = file.read().split()
    
    for req in reqs:
        try:
            print("[*] Installing " + req)
            cmd("pip install " + req)
        except Exception as e:
            print("[!] Error installing " + req)
            print(str(e))


# mains
if __name__ == "__main__":
    try:
        main()
    except ModuleNotFoundError as e:
        install(e)
    except KeyboardInterrupt:
        print("\n[exitted]")

    print("\nPLEASE RUN AGAIN AFTER INSTALLING ALL THE REQUIREMENTS")
