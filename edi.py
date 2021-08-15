import os
import sys # for argument handling
import curses # ncurses
import re # RegEx
import locale # encoding
import signal # For blocking of ctrl-c interrupt
from curses import wrapper # wrapper to run ncurses with standard error handling and stuff

#============================ Ctrl-c handling ===============================#
def catch_ctrl_C(signum, frame):
    pass
    # do nothing when interrupted lol
signal.signal(signal.SIGINT, catch_ctrl_C)

#============================ Initialized values ============================#
filename = ""
files = os.listdir()
pad_y = 0
pad_x = 0

locale.setlocale(locale.LC_ALL, '')
code = locale.getpreferredencoding()

def main(stdscr):
    stdscr.refresh()
    global files
    global filename
    global pad_y
    global pad_x
    # Pad init
    pad = curses.newpad(curses.LINES, curses.COLS)

    stdscr.leaveok(False) # Make it so the cursor coordinates are correct/generally work
    curses.set_tabsize(4)

#============================ Argument handling ============================#
    arguments = sys.argv
    if len(arguments) > 2: # Checks if there are more than one argument. If there is, an error is given.
        exit("Error: Too many arguments")
    elif len(arguments) == 2: # If one argument is given, open the file that is given as an argument
        filename = arguments[1]
        if filename in files:
            f = open(filename)
            contents = f.readlines()
            f.close()
            maxlen = 0 
            for i in contents:
                if len(i) > pad.getmaxyx()[1] - 1: # x handling
                    if len(i) > maxlen:
                        maxlen = len(i)
                        pad.resize(pad.getmaxyx()[0], maxlen)
                if curses.getsyx()[0] == curses.LINES - 1: #y handling
                    pad_y += 1
                    pad.resize(pad.getmaxyx()[0] + pad_y, pad.getmaxyx()[1])
                pad.addstr(i)
                pad.refresh(pad_y, pad_x, 0, 0, curses.LINES - 1, curses.COLS - 1)
            pad_y = 0
            pad.refresh(pad_y, pad_x, 0, 0, curses.LINES - 1, curses.COLS - 1)
            pad.move(0, 0)
        else:
            create = open(filename, "w")
            create.close()

#==================================== Functions ====================================#
    def save_close():
        global code
        global filename
        contents = []
        for y in range (pad.getmaxyx()[0]):
            contents.append(pad.instr(y,0).decode("utf-8"))
        # instr doesn't really work for more than one line and is quite impractical
        pad.clear()
        pad.refresh(pad_y, pad_x, 0, 0, curses.LINES - 1, curses.COLS - 1)
        curses.endwin()

        if filename == "": # Ask about the name of the file if the file isn't one that has been opened
            nameFound = False
            while not nameFound:
                tempfilename = input("Which file name/path do you want? ")
                validAnswer = False
                while not validAnswer:
                    answer = input("Are you sure? (y/n) ")
                    if answer == "y" or answer == "Y":
                        filename = tempfilename
                        nameFound = True
                        validAnswer = True
                    elif answer == "n" or answer == "N":
                        print("Enter another name")
                        validAnswer = True
                    else:
                        print("Invalid answer. Try again")

        create = open(filename, "w")
        create.close()
        save = open(filename, "a")

        index = 0 # Marks the index after the last index that holds a non-blank string
        curindex = 0
        for s in contents: # Find EOF by finding last non-blank string
            if not re.search("^\s*$", s): # If the string isn't only white space
                # Update index so it becomes the index after the non-empty string
                index = curindex + 1
            curindex += 1 # Update current index for next iteration

        for x in range(index, len(contents)):
            del contents[index] # Remove all the strings after EOF

        for s in contents:
            save.write(re.sub("\s*$", "", s))

        save.close()
        exit()
    # TODO: deleting past the current line
    def delete(): # Doesn't work with the default GNOME terminal
        global pad_x
        if cursorx > 0: # preventing crash
            if screenx == 0:
                if pad_x > 1:
                    pad_x -= 2
                    pad.refresh(pad_y, pad_x, 0, 0, stdscr.getmaxyx()[0] - 1, stdscr.getmaxyx()[1] - 1)
                elif pad_x > 0:
                    pad_x -= 1
                    pad.refresh(pad_y, pad_x, 0, 0, stdscr.getmaxyx()[0] - 1, stdscr.getmaxyx()[1] - 1)
            pad.delch(cursory, cursorx - 1) # Delete the character that is one to the

    def back_delete():
        pad.delch(cursory, cursorx) # Delete the character to the righ. This also
        # moves the other characters on that line one closer to the cursor

    def left():
        global pad_x
        if cursorx > 0:
            if screenx == 0:
                if pad_x > 0:
                    pad_x -= 1
                    pad.refresh(pad_y, pad_x, 0, 0, stdscr.getmaxyx()[0] - 1, stdscr.getmaxyx()[1] - 1)
            newx = cursorx - 1
            pad.move(cursory, newx)

    def right(): 
        global pad_x 

        if screenx == stdscr.getmaxyx()[1] - 1:
            pad_x += 1
        if cursorx == pad.getmaxyx()[1] - 1: 
            pad.resize(pad.getmaxyx()[0], pad.getmaxyx()[1] + 1)
        newx = cursorx + 1
        pad.move(cursory, newx)
        pad.refresh(pad_y, pad_x, 0, 0, stdscr.getmaxyx()[0] - 1, stdscr.getmaxyx()[1] - 1)

    def up():
        global pad_y
        if cursory != 0:
            if screeny == 0:
                if pad_y != 0:
                    pad_y -= 1
                    pad.refresh(pad_y, pad_x, 0, 0, stdscr.getmaxyx()[0] - 1, stdscr.getmaxyx()[1] - 1)
            newy = cursory - 1
            pad.move(newy, cursorx)

    def down(): 
        global pad_y
        if screeny == stdscr.getmaxyx()[0] - 1:
            pad_y += 1
        if cursory == pad.getmaxyx()[0] - 1:
            pad.resize(pad.getmaxyx()[0] + 1, pad.getmaxyx()[1])
        newy = cursory + 1
        pad.move(newy, cursorx)
        pad.refresh(pad_y, pad_x, 0, 0, stdscr.getmaxyx()[0] - 1, stdscr.getmaxyx()[1] - 1)

#==================================== Editing ====================================#
    while True: #Text editor loop
        pad.refresh(pad_y, pad_x, 0, 0, stdscr.getmaxyx()[0] - 1, stdscr.getmaxyx()[1] - 1)
        cursorlist = list(pad.getyx()) # Gets the current cursor position on the pad. y first, x last
        cursorx= cursorlist[1]
        cursory = cursorlist[0]
        screeny = curses.getsyx()[0]
        screenx = curses.getsyx()[1]
        try:
            key = stdscr.get_wch()
        except curses.error:
            key = -1

#==================================== Function keys ====================================#
        if key == 265: # F1
            exit() # exit without saving

        elif key == 266: # F2
            save_close() # Saves the file with the content to a user specified file.

        elif key == 267: # F3
            pass

        elif key == 268: # F4
            pass

        elif key == 263: # Backspace
        # Doesn't work with the default GNOME terminal //TODO make it universal
            delete()

        elif key == 330: #Delete-key
            back_delete()

#==================================== Cursor keys ====================================#
        elif key == 260: # Left key
            left()

        elif key == 261: # Right key
            right()

        elif key == 259: # Up key
            up()

        elif key == 258: # Down key
            down()

        elif key == 410: # Resize event
            curses.update_lines_cols()
            if curses.LINES > pad.getmaxyx()[0]:
                pad.resize(curses.LINES, pad.getmaxyx()[1])
            if curses.COLS > pad.getmaxyx()[1]: 
                pad.resize(pad.getmaxyx()[0], curses.COLS)

        elif key == -1: # No key has been registered
            pass

        elif str(key) == None:
            pass 

        else:
            key_char = str(key)
            linelength = len(re.sub("\s*$", "", pad.instr(cursory, cursorx).decode("utf-8")))
            if key_char == "\n":
                if screeny == stdscr.getmaxyx()[0] - 1:
                    pad_y += 1 
                if cursory == pad.getmaxyx()[0] - 1:
                    pad.resize(pad.getmaxyx()[0] + 1, pad.getmaxyx()[1])
            # scrolls pad to the right if cursor is at right edge
            if screenx == stdscr.getmaxyx()[1] - 1:
                pad_x += 1
            # expands pad if max x is reached 
            if cursorx == pad.getmaxyx()[1] - 1: 
                pad.resize(pad.getmaxyx()[0], pad.getmaxyx()[1] + 1)
            if cursorx + len(key_char) + linelength > pad.getmaxyx()[1] - 1:
                pad.resize(pad.getmaxyx()[0], cursorx + len(key_char) + linelength + 1)
            pad.insstr(key_char) # Add input to the screen
            pad.move(cursory, cursorx + 1)
if __name__ == '__main__':
    wrapper(main)