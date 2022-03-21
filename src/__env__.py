# COMMANDS (command, usage)
LIST = (
    "list",
    "list\t\tlist running processes"
)
TIME_CS = (
    "time-cs",
    "time-cs <t>\tt : interval timeout for accessing the CS (t > 10)"
)
TIME_P = (
    "time-p",
    "time-p <t>\tt : interval timeout for moving between states (t > 5)"
)
EXIT = (
    "exit",
    "exit\t\tquit the program execution"
)

COMMANDS = {
    LIST[0]: LIST,
    TIME_CS[0]: TIME_CS,
    TIME_P[0]: TIME_P,
    EXIT[0]: EXIT
}

# STATES
DO_NOT_WANT = "DO-NOT-WANT"
WANTED = "WANTED"
HELD = "HELD"
