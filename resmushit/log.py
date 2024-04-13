from colorama import Fore, Style, init
from datetime import datetime
from sys import stdout

init()


class Log:
    __colors = {
        "red": Fore.RED,
        "green": Fore.GREEN,
        "white": Fore.WHITE,
        "blue": Fore.BLUE,
    }

    def __init__(self, quiet_mode) -> None:
        self.quiet_mode = quiet_mode

    def log(self, message, color="white"):
        if not self.quiet_mode:
            print(
                Log.__colors.get(color, "white")
                + f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} {message}"
                + Style.RESET_ALL
            )
