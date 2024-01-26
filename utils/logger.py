from rich.logging import RichHandler
import logging

class Logger:
    def __init__(self, name: str, level: str = "DEBUG"):
        self.logger = logging.getLogger(name)
        
        # Removing any default handlers to avoid duplicate logs
        for handler in self.logger.handlers[:]:
            self.logger.removeHandler(handler)

        # Setting up the rich handler
        rich_handler = RichHandler()
        formatter = logging.Formatter('%(message)s')
        rich_handler.setFormatter(formatter)
        self.logger.addHandler(rich_handler)
        self.logger.setLevel(level)

    def debug(self, message: str):
        self.logger.debug(message)

    def info(self, message: str):
        self.logger.info(message)

    def warning(self, message: str):
        self.logger.warning(message)

    def error(self, message: str):
        self.logger.error(message)


