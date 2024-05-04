from datetime import datetime
from sys import stdout

class Log:

    def __init__(self, quiet_mode) -> None:
        self.quiet_mode = quiet_mode

    def log(self, message):
        if not self.quiet_mode:
            print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} {message}")
