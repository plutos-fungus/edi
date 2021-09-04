# TODO
## Not finished
- Vi mode?
- Fix program lock-up after a random amout of ctrl-key and any character combination
- Delete past the current line (semi working)

## Finished
- If file passed as argument doesn't exist, create file
- Fix out of bounds errors
- Remove options to ungracefully exit (such as ctrl+c) - some, like ctrl-z still remain
- Switch from an ncurses screen to an ncurses pad in order to have more "space" for editing - implemented scrolling
- Loading files bigger than the terminal emulator
- UTF-8 support and proper string conversion when saving
- Moving functions from edi.py to separate handling files
- Read config file for color?
