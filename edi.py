import os
import sys # for argument handling
import curses # ncurses
import re # RegEx
import locale # encoding
from curses import wrapper # wrapper to run ncurses with standard error handling and stuff

#============================ Initialized values ============================#
filename = ""
files = os.listdir()
locale.setlocale(locale.LC_ALL, '')
code = locale.getpreferredencoding()

def main (stdscr):
    global files
    global filename
    stdscr.leaveok(False) # Make it so the cursor coordinates are correct/generally work
    curses.set_tabsize(4)
    #stdscr.scrollok(True)
    #stdscr.idlok(True)

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
            for i in contents:
                stdscr.addstr(i)
        else:
            create = open(filename, "w")
            create.close()

#==================================== Functions ====================================#
    def save_close():
        global code
        global filename
        contents = []
        newcontents = [] # Stores new contents list after RegEx
        for y in range (stdscr.getmaxyx()[0]):
            contents.append(str(stdscr.instr(y,0)))
        # instr doesn't really work for more than one line and is quite impractical
        stdscr.clear()
        stdscr.refresh()
        curses.endwin()

        if filename == "": # Ask about the name of the file if the file isn't one that has been opened
            nameFound = False
            while not nameFound:
                print("Which file name/path do you want?")
                tempfilename = input("")
                print("Are you sure? (y/n)")
                answer = input("")
                validAnswer = False
                while not validAnswer:
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
    # TODO: deleting past the current line
    def delete(): # Doesn't work with the default GNOME terminal
        if cursorx != 0: # Preventing crash
            stdscr.delch(cursory, cursorx - 1) # Delete the character that is one to the

    def back_delete():
        stdscr.delch(cursory, cursorx) # Delete the character to the righ. This also
        # Moves the other characters on that line one closer to the cursor

    def left():
        if cursorx != 0:
            newx = cursorx - 1
        else:
            newx = cursorx
        stdscr.move(cursory, newx)

    def right(): # TODO: OOB avoidance // temporarily fixed
        if cursorx != stdscr.getmaxyx()[1] - 1:
            newx = cursorx + 1
        else:
            newx = cursorx
        stdscr.move(cursory, newx)

    def up():
        if cursory != 0:
            newy = cursory - 1
        else:
            newy = cursory
        stdscr.move(newy, cursorx)

    def down(): # TODO: OOB avoidance (temp fix)
        if cursory != stdscr.getmaxyx()[0] - 1:
            newy = cursory + 1
        else:
            newy = cursory
        stdscr.move(newy, cursorx)

#==================================== Editing ====================================#
    while True: #Text editor loop
        stdscr.refresh() # Refresh the screen, so the commands that are being send to stdscr
        # actually gets executed
        cursorlist = list(curses.getsyx()) # Gets the current cursor position. y first, x last
        cursorx = cursorlist[1]
        cursory = cursorlist[0]
        key = stdscr.get_wch()

#==================================== Function keys ====================================#
        if key == 265: # F1
            exit() # exit without saving

        if key == 266: # F2
            save_close() # Saves the file with the content to a user specified file.

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
            pass

        else:
            stdscr.addstr(str(key)) # Add input to the screen

wrapper(main)
