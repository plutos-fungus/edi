import os
import sys # for argument handling
import curses # ncurses
import re
from curses import wrapper # wrapper to run ncurses with standard error handling and stuff
import keyboard

global filename
filename = ""
global liststr
liststr = []

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
            s = re.sub("\'", "", s)
            s = re.sub("^b", "", s)
            s = re.sub("\s*$", "\n", s)
            #news = re.sub("\s{10,}", "", s) # If there is more than 10 whitespace, replace them with no whitespace
            #s = re.sub("\'b\'", "\n", news)
            save.write(s)
        #for y in range (stdscr.getmaxyx()[1]):

        save.close()
        #hej = str(contents)
        #liststr.append(hej)
        #for i in liststr:
            #save.write(i)
            #save.close()
        #save.write(str(contents)) # Convert the row of bytes to a string and save it //TODO converte to a list of characters pr. row
        #save.close()
        exit()

    def delete(): # Doesn't work with the default GNOME terminal
        if cursorx != 0: # preventing crash
            stdscr.delch(cursory, cursorx - 1) # Delete the character that is one to the left from the cursor

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
        stdscr.refresh() # Refresh the screen, so the commands that are being send to stdscr actually gets executed
        cursorlist = list(curses.getsyx()) # Gets the current cursor position. y first, x last
        cursorx = cursorlist[1]
        cursory = cursorlist[0]
        input = stdscr.getkey()

#==================================== Function keys ====================================#
        if input == "KEY_F(1)": # exit without saving
            exit()

        if input == "KEY_F(2)": # Saves the file with the content to a file named "testing". //TODO: input filename
            save_close()

        elif input == "KEY_BACKSPACE": # Doesn't work with the default GNOME terminal
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
