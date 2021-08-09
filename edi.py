import os
import sys # for argument handling
import curses # ncurses
import re
from curses import wrapper # wrapper to run ncurses with standard error handling and stuff

global filename
filename = ""

def main (stdscr):
    stdscr.leaveok(False) # Make it so the cursor coordinates are correct

#============================Argument handling ============================#
    arguments = sys.argv
    if len(arguments) > 2: # Checks if there are more than one argument. If there is, an error is given.
        exit("Error: Too many arguments")
    elif len(arguments) == 2: # If one argument is given, open the file that is given as an argument
        filename = arguments[1]
        f = open(filename)
        contents = f.readlines()
        f.close()
        for i in contents:
            stdscr.addstr(i)

#==================================== Functions ====================================#
    def save_close():
        contents = []
        newcontents = [] # Stores new contents list after RegEx
        for y in range (stdscr.getmaxyx()[0]):
            contents.append(str(stdscr.instr(y,0)))
        # instr doesn't really work for more than one line and is quite impractical
        stdscr.clear()
        stdscr.refresh()
        filename = "testing"
        create = open(filename, "w")
        create.close()
        save = open(filename, "a")
        for s in contents: # Do some RegEx stuff
            s = re.sub("\'", "", s) # Find "'" and remove it
            s = re.sub("^b", "", s) # Find all "b" at beginning of line and remove it
            s = "".join(s.rstrip()) # Strip all white space to the right of line
            s = s + "\n" # Add newline to each line as it has just been removed
            newcontents.append(s) # Store strings that pass the RegEx test in new list

        index = 0 # Marks the index after the last index that holds a non-blank string
        curindex = 0
        for s in newcontents: # Find EOF by finding last non-blank string
            if not re.search("^\s*$", s): # If the string isn't only white space
                # Update index so it becomes the index after the non-empty string
                index = curindex + 1
            curindex += 1 # Update current index for next iteration

        for x in range(index, len(newcontents)):
            del newcontents[index] # Remove all the strings after EOF

        for s in newcontents:
            save.write(s)

        save.close()
        exit()

    def delete(): # Doesn't work with the default GNOME terminal
        if cursorx != 0: # preventing crash
            stdscr.delch(cursory, cursorx - 1) # Delete the character that is one to the
            # left from the cursor

    def left():
        if cursorx != 0:
            newx = cursorx - 1
        else:
            newx = cursorx
        stdscr.move(cursory, newx)

    def right():
        newx = cursorx + 1
        stdscr.move(cursory, newx)

    def up():
        if cursory != 0:
            newy = cursory - 1
        else:
            newy = cursory
        stdscr.move(newy, cursorx)

    def down():
        newy = cursory + 1
        stdscr.move(newy, cursorx)

#==================================== Editing ====================================#
    while True: #Text editor loop
        stdscr.refresh() # Refresh the screen, so the commands that are being send to stdscr
        # actually gets executed
        cursorlist = list(curses.getsyx()) # Gets the current cursor position. y first, x last
        cursorx = cursorlist[1]
        cursory = cursorlist[0]
        input = stdscr.getkey()

#==================================== Function keys ====================================#
        if input == "KEY_F(1)": # exit without saving
            exit()

        if input == "KEY_F(2)": # Saves the file with the content to a file named "testing".
        # //TODO input filename
            save_close()

        elif input == "KEY_BACKSPACE": # Doesn't work with the default GNOME terminal //TODO make
        # it universal
            delete()

#==================================== Cursor keys ====================================#
        elif input == "KEY_LEFT":
            left()

        elif input == "KEY_RIGHT":
            right()

        elif input == "KEY_UP":
            up()

        elif input == "KEY_DOWN":
            down()

        else:
            stdscr.addstr(input) # Add input to the screen

wrapper(main)
