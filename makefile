.PHONY: smallsh debug
SOURCE := smallsh.c smallshlib.c
EXECUTABLE := smallsh

smallsh: $(SOURCE)
	gcc -std=c99 -o $(EXECUTABLE) $(SOURCE)

debug: $(SOURCE)
	gcc -g -std=c99 -o $(EXECUTABLE) $(SOURCE)

# IFS=$' '$'\t'$'\n' PS1='$ ' ./smallsh