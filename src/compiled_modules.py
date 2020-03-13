'''

This file is meant for generating ahead of time compiled functions that accelerate code performance by reducing constants for simple functions that
are invoked for roughly every letter in a document

For instance, some characters such as inverted commas are handled differently by docx files.

'''

from numba.pycc import CC 
from numba import types
cc = CC('check_letter')
cc.verbose = True

@cc.export('check_inv', types.boolean(types.string))
def check_inv(letter):
    if letter == '‘' or letter == '’' or letter == "'":
        return True
    else:
        return False

@cc.export('check_dinv', types.boolean(types.string))
def check_dinv(letter):
    if letter == '“' or letter == '”' or letter == '"':
        return True
    else:
        return False

@cc.export('check_hyphen', types.boolean(types.string))
def check_hyphen(letter):
    if letter == '-' or letter == '–':
        return True
    else:
        return False

cc.compile()