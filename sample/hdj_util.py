from colorama import init, Fore, Back, Style

init()

"""
Prints out the version of the software
"""


def version():
    print(
        Style.BRIGHT
        + Back.BLUE
        + Fore.GREEN
        + "He's Dead, Jim. The Python based link-checker. "
        + Fore.BLACK
        + "Version 0.1.05"
    )
