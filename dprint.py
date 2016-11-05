"""dprint.py: prints with."""

__author__ = "Alex 'Chozabu' P-B"
__copyright__ = "Copyright 2016, Chozabu"

from inspect import currentframe, getframeinfo
import inspect



def dprint(*args):
    print(*args)
    return
    from settings import machine_name
    (frame, filename, line_number,
     function_name, lines, index) = inspect.getouterframes(inspect.currentframe())[3]
    pa = "---" + machine_name + '\033[91m' + filename + ":" + str(line_number) + " " + function_name + '\x1b[0m'
    (frame, filename, line_number,
     function_name, lines, index) = inspect.getouterframes(inspect.currentframe())[2]
    pb = "---"+machine_name + '\033[91m' + filename + ":" + str(line_number) + " " + function_name + '\x1b[0m'
    (frame, filename, line_number,
     function_name, lines, index) = inspect.getouterframes(inspect.currentframe())[1]
    print()
    print(pa)
    print(pb)
    print(machine_name + '\033[91m' + filename + ":" + str(line_number) + " " + function_name + '\x1b[0m')
    print(str(args))
