#define _POSIX_C_SOURCE 200809L
#define _GNU_SOURCE

#include <err.h>                                                                                                                                  
#include <errno.h>                                                                                                                                
#include <getopt.h>                                                                                                                               
#include <stdio.h>                                                                                                                                
#include <stdlib.h>
#include <unistd.h>
#include <stdint.h>
#include <sys/wait.h>
#include <sys/types.h>
#include <string.h>
#include "smallshlib.h"

int
main(void)
{
  
  char const *PS1 = getenv("PS1");
  char const *IFS = getenv("IFS") ? getenv("IFS") : " \t\n";
  char *line = NULL;
  char *token;
  size_t n = 0;
  ssize_t read;
  char *wordList = NULL;
  size_t *wordCount = 0;
  
  while (1) {
    
    /* Manage Background Processes */


    /* Prompt & Read Line of Input */
restartPrompt:
    fprintf(stderr, "%s", PS1);
    read = getline(&line, &n, stdin);
    if (read == -1) {
      err(errno, "getline error");
      goto restartPrompt;
    }
    

    /* Word Tokenization & Storage */
    token = strtok(line, IFS);
    while (token) {

      // Stops tokenizing if remaining text is commented with hash symbol.
      if (strncmp(token, "#", 1) == 0) break;

      // Stored Token
      printf("Storing token: %s\n", token);
      char *dupToken = strdup(token);
      // Add to array
      process_token(&wordList, wordCount, dupToken);
      free(dupToken);

      token = strtok(NULL, IFS);
      if (!token) {
        break;
      }
    }





























    /* Parse commands */



    /* Execution & Built-In Commands */


    /* Execution & Non-Built-In Commands */



    /* Waiting & Signal Handling */


  };

  free(line);

  exit(EXIT_SUCCESS);
  
}

