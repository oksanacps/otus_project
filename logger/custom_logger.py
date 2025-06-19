import logging
import sys
import types
import uuid


def _log_newline(self, how_many_lines=1):
    # Switch formatter, output a blank line
    self.handler.setFormatter(self.blank_formatter)

    for i in range(how_many_lines):
        self.info("")

    # Switch back
    self.handler.setFormatter(self.formatter)


logger = logging.getLogger("logger")
logger.setLevel(level=getattr(logging, "DEBUG"))

formatter = logging.Formatter(fmt="[%(asctime)s: %(levelname)s] %(message)s")
blank_formatter = logging.Formatter(fmt="")

handler = logging.StreamHandler(stream=sys.stdout)
handler.setFormatter(formatter)
logger.addHandler(handler)

logger.handler = handler
logger.formatter = formatter
logger.blank_formatter = blank_formatter
logger.newline = types.MethodType(_log_newline, logger)

event_id = str(uuid.uuid4())
logger.info('Установлен уровень логирования: "DEBUG".')
