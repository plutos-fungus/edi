import sys # for argument handling
import curses # ncurses
import re # RegEx
import locale # encoding
import signal # For blocking of ctrl-c interrupt
#import viMode # Pretty self explanatory
from fileInteractions import * 
from keyActions import *
from keyHandling import handlekeys
from config_handler import *
from curses import wrapper # wrapper to run ncurses with standard error handling and stuff
from globalDefinitions import *

#============================ Ctrl-c handling ===============================#
def catch_ctrl_C(signum, frame):
    pass
    # do nothing when interrupted lol
signal.signal(signal.SIGINT, catch_ctrl_C)

#============================ Initialized values ============================#
locale.setlocale(locale.LC_ALL, '')
code = locale.getpreferredencoding()

def main(stdscr):
    myPad = Pad()
    cursor = Cursor()
    curses.start_color()
    stdscr.refresh()
    tabsize = 4 # tab size used by curses

    # Pad init
    pad = curses.newpad(curses.LINES, curses.COLS)

    stdscr.leaveok(False) # Make it so the cursor coordinates are correct/generally work
    curses.set_tabsize(tabsize)

#============================ Argument handling ============================#
    arguments = sys.argv
    filename = loadfile(pad, myPad, arguments)
    opperators = getSyntax(filename)

#============================ Color setup ==================================#
    myColors = Themestuff()  
    colors_list = myColors.parseColors()

    for x in range(8):
        curses.init_color(x, colors_list[x][0], colors_list[x][1], colors_list[x][2])

    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)
    fileSyntax(pad, opperators)

#==================================== Editing ====================================#
    while True: #Text editor loop
        pad.refresh(myPad.posy, myPad.posx, 0, 0, stdscr.getmaxyx()[0] - 1, stdscr.getmaxyx()[1] - 1)
        cursorlist = list(pad.getyx()) # Gets the current cursor position on the pad. y first, x last
        cursor.px = cursorlist[1]
        cursor.py = cursorlist[0]
        cursor.sx = curses.getsyx()[1]
        cursor.sy = curses.getsyx()[0]
        eol = re.sub("\s*$", "", pad.instr(cursor.py, cursor.px).decode("utf-8"))
        linelength = len(eol)
        syntaxHighlight(pad, myPad, stdscr, cursor, opperators)
        try:
            key = stdscr.get_wch()
        except curses.error:
            key = -1
        handlekeys(pad, myPad, stdscr, cursor, linelength, eol, tabsize, filename, key, opperators)
        
if __name__ == '__main__':
    wrapper(main)