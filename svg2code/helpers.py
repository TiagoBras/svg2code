import re

def promptYesOrNo(message):
    while True:
        m = re.match(r'(y|yes)|(n|no)', raw_input(message + " "), re.IGNORECASE)

        if m is None:
            print("Please insert any of the possible options: [yes, y, no, y] (case insensitive)")
        else:
            return m.group(1) is not None