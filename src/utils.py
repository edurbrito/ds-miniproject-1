from __env__ import *


def isvalid_command(args):

    if args[0] not in COMMANDS or not (1 <= len(args) <= 2):
        return False

    if args[0] == TIME_CS[0] or args[0] == TIME_P[0]:
        if len(args) != 2 or not args[1].isnumeric():
            return False
        if args[0] == TIME_CS[0] and int(args[1]) < 10:
            return False
        if args[0] == TIME_P[0] and int(args[1]) < 5:
            return False

    return True


def print_usage(msg=""):
    if msg != "":
        print(msg)
    print("Available commands: ")
    for c in COMMANDS:
        print(COMMANDS[c][1])
