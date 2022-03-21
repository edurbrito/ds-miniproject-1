import sys
import readline  # for key up support
from utils import *

if len(sys.argv) != 2 or not sys.argv[1].isnumeric() or int(sys.argv[1]) < 1:
    print("Usage:  ricartagrawla.sh [N]\n\tN\tnumber of processes (N > 0)")
    exit(1)

# start processes here

print_usage()


def list():
    print("HERE")


def time_cs(t):
    print("HERE")


def time_p(t):
    print("HERE")


while True:

    command = input("\nCommand: ")

    args = command.split(" ")

    if not isvalid_command(args):
        print_usage("Command Invalid...\n")
        continue
    elif args[0] == LIST[0]:
        list()
    elif args[0] == TIME_CS[0]:
        time_cs(args[1])
    elif args[0] == TIME_P[0]:
        time_p(args[1])
    elif args[0] == EXIT[0]:
        print("Exiting...")
        exit(0)
