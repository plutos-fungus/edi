import os
import curses
from curses import wrapper




def main (stdscr):
    stdscr.leaveok(False) # gør sådan at cursor koordinaterne faktisk er korrekte

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

    def delete():
        # Den er ikke glad for delete koden
        pass

    while True: #Text editor loop
        stdscr.refresh() # refresh skærmen, sådan at de kommandoer, som sendes til stdscr, rent faktisk udføres
        cursorlist = list(curses.getsyx()) # får nuværende cursor posytion, y først, x sidst
        cursorx = cursorlist[1]
        cursory = cursorlist[0]
        input = stdscr.getkey()

        if input == "KEY_F(1)": # exit without saving
            break

        if input == "KEY_F(2)": # gem fil med indhold til en fil ved navn testing. TODO: input filnavn
            save_close()

        elif input == "KEY_BACKSPACE": # Broken as of now
            if cursorx != 0: # preventing crash
                stdscr.delch(cursory, cursorx - 1) # slet karakteren, som er en til venstre for cursoren.


            #cursor flytte kode
        elif input == "KEY_LEFT":
            if cursorx != 0:
                newx = cursorx - 1

            else:
                newx = cursorx
            stdscr.move(cursory, newx)

        elif input == "KEY_RIGHT":
            newx = cursorx + 1
            stdscr.move(cursory, newx)

        elif input == "KEY_UP":
            if cursory != 0:
                newy = cursory - 1

            else:
                newy = cursory
            stdscr.move(newy, cursorx)

        elif input == "KEY_DOWN":
            newy = cursory + 1
            stdscr.move(newy, cursorx)

        else:
            stdscr.addstr(input) # tilføj input til skærmen

wrapper(main)
