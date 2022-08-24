import colorama
from termcolor import colored


def custom_log(msg: str, color: str) -> None:
    colorama.init()
    print(colored(f' {msg} ', color))


#def custom_log(msg: str, color: str) -> None:
#    print(msg)