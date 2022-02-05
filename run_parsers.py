from subprocess import run
import sys
import os

def run_parser(file_name):
    run([sys.executable, file_name])



if __name__ == "__main__":
    run_parser(f"{os.getcwd()}//parsers//startup_resources.py")

