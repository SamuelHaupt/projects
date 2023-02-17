.PHONY: run
SOURCE := smallsh.c smallshlib.c
EXECUTABLE := smallsh

smallsh: $(SOURCE)
  	gcc -std=c99 -o $(EXECUTABLE) $(SOURCE)