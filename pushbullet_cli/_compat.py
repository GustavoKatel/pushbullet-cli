import sys

PY2 = sys.version_info[0] == 2

if PY2:

    read_line = raw_input

else:

    read_line = input

__all__ = ['read_line']
