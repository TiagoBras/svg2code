from __future__ import absolute_import, division, print_function

try: 
    input = raw_input
except NameError: 
    pass

import re

def promptYesOrNo(message):
    while True:
        m = re.match(r'(y|yes)|(n|no)', input(message + " "), re.IGNORECASE)

        if m is None:
            print("Please insert any of the possible options: [yes, y, no, y] (case insensitive)")
        else:
            return m.group(1) is not None