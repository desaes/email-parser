import colorama
from termcolor import colored
from datetime import datetime


def custom_log(msg: str, color: str) -> None:
    colorama.init()
    print(colored(f'{datetime.now()} - {msg} ', color))


#def custom_log(msg: str, color: str) -> None:
#    print(msg)