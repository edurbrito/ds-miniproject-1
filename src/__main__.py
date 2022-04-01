import rpyc
import sys
import readline  # for key up support
from utils import *

if len(sys.argv) != 2 or not sys.argv[1].isnumeric() or int(sys.argv[1]) < 1:
    print("Usage:  ./client.sh [N]\n\tN\tnumber of processes (N > 0)")
    exit(1)

conn = rpyc.connect("localhost", 18812)

conn.root.start(int(sys.argv[1]))

print_usage()

while True:

    command = input("\nCommand: ")

    args = command.split(" ")

    if not isvalid_command(args):
        print_usage("Command Invalid...\n")
        continue
    elif args[0] == LIST[0]:
        print(conn.root.list())
    elif args[0] == TIME_CS[0]:
        print(conn.root.time_cs(int(args[1])))
    elif args[0] == TIME_P[0]:
        print(conn.root.time_p(int(args[1])))
    elif args[0] == EXIT[0]:
        print("Exiting...")
        exit(0)
