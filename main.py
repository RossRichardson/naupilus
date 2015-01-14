#!/usr/bin/python

"""
Interactive Python Menu System. The aim here is for a simple yet conventient menu system with a few nice features.
Another goal is to minimise any dependencies on using external libraries.

Initial base code released to github. 
@author: Ross Richardson

Note: this is mix licensed.
Getch class code is PSF. http://code.activestate.com/recipes/134892/
The rest is GPLv2
"""

"""
Menu Header
 [1] Item 1.. 
  2  Item 2..
  3  Item 3..
  4  Exit
"""

menu = ["Menu Header",
        "Item 1..",
        "Item 2..",
        "Item 3..",
        "Exit"]
        
        
"""
\033[93m     # yellow text - transparent background
\033[95m     # purple text - transparent background
\033[01;46m  # white text - cyan background
\033[01;41m  # white text - red background
"""

WHITE_FG_CYAN_BG_STR = "\033[01;46m"
RESET_COL_STR = "\033[0m"
CLEAR_SCROLLBACK_STR = "\033c"

import sys, tty, termios

class _Getch:
    """Gets a single character from standard input.  Does not echo to the screen."""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()


class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()


def read_key():
    
    getch = _Getch()
    key = ''
    three = ''
    
    while(True):
        
        key = getch()
        
        # SINGLE KEYS
        # store into three string..
        if len(three) <= 3 and ((key == '\x1b') or (key == '[') or (key == 'A') or (key == 'B')):
            three = three + key
        elif key == '\r': # ENTER
            return 0
        else:
            three = ''
        
        # UP or DOWN KEYS
        if three == '\x1b[A': # UP
            return -1
        elif three == '\x1b[B': # DOWN
            return 1
        

def print_menu(menu, selected):
    
    print CLEAR_SCROLLBACK_STR + menu[0]
    for index in range(1,len(menu)):
        if selected == index:
            print WHITE_FG_CYAN_BG_STR + ("[%s] " % index),
        else:
            print " %s  " % index,
        print menu[index] + RESET_COL_STR
    
def navigate_menu(selected, key_value):
    """ navigate and adjust for cycling """
    selected += key_value
    
    # cycling correction
    if selected < 1:
        selected = len(menu_1)-1
    elif selected > len(menu_1)-1:
        selected = 1
    
    return selected
    
   
###
### start here
###
    
selected = 1 # default
while(True):
    
    print_menu(menu_1, selected)
    key_value = read_key()
    
    # ON SELECTION/ENTER KEY
    if key_value == 0:
        
        if menu_1[selected] == 'Exit':
            sys.exit(0)
        
        # process other menu items
    
    # UP AND DOWN MOVEMENT
    selected = navigate_menu(selected, key_value)
