
from dataclasses import dataclass


@dataclass
class bgColors():
    green = "\033[32m"
    red = "\033[31m"
    reset = "\033[0m"
    yellow = "\033[93m"
    magenta = "\033[95m"
    cyan = "\033[96m"


def print_helper(message: str, color: str = bgColors.magenta) -> None:
    print(color + message + bgColors.reset)