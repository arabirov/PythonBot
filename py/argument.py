import re

command_re = re.compile(r"^/\w+\s+(\d+)+$")


def extract_arg(message):  # ----- S H I T C 0 D E -----
    if command_re.match(message.text):
        return command_re.match(message.text).group(1)
    else:
        return 0
