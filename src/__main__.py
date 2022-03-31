import readline  # for key up support
import signal
import sys
from logging import CRITICAL, DEBUG, ERROR, INFO, basicConfig

import rpyc

from node import Node
from utils import *

if len(sys.argv) != 2 or not sys.argv[1].isnumeric() or int(sys.argv[1]) < 1:
    print("Usage: run.sh [N]\n\tN\tnumber of processes (N > 0)")
    exit(1)


basicConfig(filename="./log.out", filemode="w", level=DEBUG)


N = int(sys.argv[1])

nodes = []

for n in range(N):
    nodes.append(Node(PORT + n, N))

for n in nodes:
    n.start()


def signal_handler(sig, frame):
    for n in nodes:
        n.terminate()
    print("Exiting...")
    exit(0)


signal.signal(signal.SIGINT, signal_handler)


print_usage()


def list():
    result = []
    for n in nodes:
        conn = rpyc.connect("localhost", n.port)
        result.append(str(conn.root.get_state()))
        conn.close()
    return "\n".join(result)


def time_cs(t):
    if str(t).isnumeric() and int(t) >= 10:
        for n in nodes:
            conn = rpyc.connect("localhost", n.port)
            if not conn.root.set_timeout_cs(int(t)):
                conn.close()
                return "Invalid t"
            conn.close()
        return f"Timeout interval for CS changed to [{10}, {t}]."
    return "Invalid t"


def time_p(t):
    if str(t).isnumeric() and int(t) >= 5:
        for n in nodes:
            conn = rpyc.connect("localhost", n.port)
            if not conn.root.set_timeout_p(int(t)):
                conn.close()
                return "Invalid t"
            conn.close()
        return f"Timeout interval for Processes changed to [{5}, {t}]."
    return "Invalid t"


while True:

    command = input("\nCommand: ")

    args = command.split(" ")

    if not isvalid_command(args):
        print_usage("Command Invalid...\n")
        continue
    elif args[0] == LIST[0]:
        print(list())
    elif args[0] == TIME_CS[0]:
        print(time_cs(args[1]))
    elif args[0] == TIME_P[0]:
        print(time_p(args[1]))
    elif args[0] == EXIT[0]:
        print("Exiting...")
        break

for n in nodes:
    n.terminate()

exit(0)
