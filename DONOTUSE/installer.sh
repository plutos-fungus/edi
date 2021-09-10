#!/bin/sh

# WARNING: Not for use with the source code; only used for the releases.

INSTALLPATH=~/.local/bin

mkdir ~/.config/edi
mkdir ~/.config/edi/languages

mv configs/* ~/.config/edi/

mv edi $INSTALLPATH