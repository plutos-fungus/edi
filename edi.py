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
from globalDefinitions import PadPos
#============================ Ctrl-c handling ===============================#
def catch_ctrl_C(signum, frame):
    pass
    # do nothing when interrupted lol
signal.signal(signal.SIGINT, catch_ctrl_C)

#============================ Initialized values ============================#

locale.setlocale(locale.LC_ALL, '')
code = locale.getpreferredencoding()

def main(stdscr):
    myPadPos = PadPos()
    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    stdscr.refresh()
    tabsize = 4 # tab size used by curses

    # Pad init
    pad = curses.newpad(curses.LINES, curses.COLS)

    stdscr.leaveok(False) # Make it so the cursor coordinates are correct/generally work
    curses.set_tabsize(tabsize)

#============================ Argument handling ============================#
    arguments = sys.argv
    filename = loadfile(pad, myPadPos, arguments)
    opperators = getOperators()
    fileSyntax(pad, opperators)

#==================================== Editing ====================================#
    while True: #Text editor loop
        pad.refresh(myPadPos.y, myPadPos.x, 0, 0, stdscr.getmaxyx()[0] - 1, stdscr.getmaxyx()[1] - 1)
        cursorlist = list(pad.getyx()) # Gets the current cursor position on the pad. y first, x last
        cursorx = cursorlist[1]
        cursory = cursorlist[0]
        screeny = curses.getsyx()[0]
        screenx = curses.getsyx()[1]
        eol = re.sub("\s*$", "", pad.instr(cursory, cursorx).decode("utf-8"))
        linelength = len(eol)
        syntaxHighlight(pad, myPadPos, stdscr, cursory, cursorx, opperators)
        try:
            key = stdscr.get_wch()
        except curses.error:
            key = -1
        #if key == 266:
            #save_close(pad, pad_y, pad_x, filename)
        handlekeys(pad, myPadPos, stdscr, cursory, cursorx, screeny, screenx, linelength, eol, tabsize, filename, key, opperators)
        


if __name__ == '__main__':
    wrapper(main)