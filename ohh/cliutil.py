def print_title(message):
    print("\033[34m:: " + message + "\033[0m")

def print_warning(message):
    print("\033[33mWarning：\033[0m" + message)

def print_error(message):
    print("\033[31mError：\033[0m" + message)

def print_info(message: str):
    for line in message.splitlines():
        print("  " + line)

def print_checking(message = 'Are you sure?') -> bool:
    while True:
        confirm_message = input(message + " [Y/n]")
        if confirm_message == "y" or confirm_message == "Y" or confirm_message == "":
            return True
        elif confirm_message == "n" or confirm_message == "N":
            return False

def DEBUG_VERSION(func):
    import sys
    if len(sys.argv) >= 2 and sys.argv[1] == "debug":
        func()

def RELEASE_VERSION(func):
    import sys
    if len(sys.argv) == 1 or sys.argv[1] != "debug":
        func()