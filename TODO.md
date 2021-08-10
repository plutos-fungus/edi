# TODO
Unfixed:
- Add UTF-8 support, both in text buffer and saving
- Streamline saving, so it's possible to save apostrophes properly
- Switch from an ncurses screen to an ncurses pad in order to have more "space" for editing
- Vi mode?
- Read config file for color?
- Fix program lock-up after a random amout of ctrl-key and any character combination
- Delete past the current line (semi working)

Fixed:
- If file passed as argument doesn't exist, create file
- Fix out of bounds errors (temp solution)
- Remove options to ungracefully exit (such as ctrl+c)
