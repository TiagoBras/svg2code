# -*- coding: utf-8 -*-
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

UNITS_RATIOS = {
  'px': 1.0, 'pt': 1.25, 'pc': 15.0, 'mm': 3.543307, 'cm': 35.43307, 'in': 90.0
}
UNITS_RE = re.compile(r'(?P<num>\d+)\s*(?P<unit>\w+)*')
def parseSVGNumber(number):
    m = UNITS_RE.match(number.lower())

    if m is None:
        raise TypeError("'%s' is not a valid number" % number)

    unit = m.group('unit') or 'px'

    if unit not in UNITS_RATIOS:
        raise TypeError("Unknow unit '%s'" % unit)

    return UNITS_RATIOS[unit] * float(m.group('num'))