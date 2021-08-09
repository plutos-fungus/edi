import os
import curses
from curses import wrapper

def main (stdscr):
    stdscr.leaveok(False) # gør sådan at cursor koordinaterne faktisk er korrekte

#==================================== Functions ====================================#
    def save_close():
        contents = stdscr.instr(0,0) # kopier skærmens tekstindhold til en række bytes
        # instr virker ikke rigtig til mere end en linje og er ret upraktisk
        stdscr.clear()
        stdscr.refresh()
        filename = "testing"
        create = open(filename, "w")
        create.close()
        save = open(filename, "a")
        save.write(str(contents)) # konverter rækken af bytes til en string og gem den
        save.close()
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
        stdscr.refresh() # refresh skærmen, sådan at de kommandoer, som sendes til stdscr, rent faktisk udføres
        cursorlist = list(curses.getsyx()) # får nuværende cursor posytion, y først, x sidst
        cursorx = cursorlist[1]
        cursory = cursorlist[0]
        input = stdscr.getkey()

#==================================== Function keys ====================================#
        if input == "KEY_F(1)": # exit without saving
            exit()

        if input == "KEY_F(2)": # gem fil med indhold til en fil ved navn testing. TODO: input filnavn
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
            stdscr.addstr(input) # tilføj input til skærmen

wrapper(main)
