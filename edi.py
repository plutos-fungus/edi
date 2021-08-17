import sys # for argument handling
import curses # ncurses
import re # RegEx
import locale # encoding
import signal # For blocking of ctrl-c interrupt
#import viMode # Pretty self explanatory
from fileInteractions import * 
from keyActions import *
from keyHandling import handlekeys
from curses import wrapper # wrapper to run ncurses with standard error handling and stuff

#============================ Ctrl-c handling ===============================#
def catch_ctrl_C(signum, frame):
    pass
    # do nothing when interrupted lol
signal.signal(signal.SIGINT, catch_ctrl_C)

#============================ Initialized values ============================#

locale.setlocale(locale.LC_ALL, '')
code = locale.getpreferredencoding()

def main(stdscr):
    stdscr.refresh()
    pad_y = 0
    pad_x = 0
    tabsize = 4 # tab size used by curses

    # Pad init
    pad = curses.newpad(curses.LINES, curses.COLS)

    stdscr.leaveok(False) # Make it so the cursor coordinates are correct/generally work
    curses.set_tabsize(tabsize)

#============================ Argument handling ============================#
    arguments = sys.argv
    filename = loadfile(pad, pad_y, pad_x, arguments)

#==================================== Editing ====================================#
    while True: #Text editor loop
        pad.refresh(pad_y, pad_x, 0, 0, stdscr.getmaxyx()[0] - 1, stdscr.getmaxyx()[1] - 1)
        cursorlist = list(pad.getyx()) # Gets the current cursor position on the pad. y first, x last
        cursorx = cursorlist[1]
        cursory = cursorlist[0]
        screeny = curses.getsyx()[0]
        screenx = curses.getsyx()[1]
        eol = re.sub("\s*$", "", pad.instr(cursory, cursorx).decode("utf-8"))
        linelength = len(eol)
        try:
            key = stdscr.get_wch()
        except curses.error:
            key = -1
        #if key == 266:
            #save_close(pad, pad_y, pad_x, filename)

        handlekeys(pad, pad_y, pad_x, stdscr, cursory, cursorx, screeny, screenx, linelength, eol, tabsize, filename, key)


if __name__ == '__main__':
    wrapper(main)
