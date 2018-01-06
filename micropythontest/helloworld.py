#!/usr/bin/env micropython

import sys
import logging

# Debug print
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

eprint("Hello, Microworld")