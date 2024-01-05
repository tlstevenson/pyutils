import sys
from os import path

this_dir = path.dirname(path.abspath(__file__))

if not this_dir in sys.path:
    sys.path.append(this_dir)