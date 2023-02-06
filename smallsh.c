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
#include <string.h>

int
main(void)
{
  
  char const *PS1 = getenv("PS1");
  char const *IFS = getenv("IFS") ? getenv("IFS") : " \t\n";
  char *line = NULL;
  char *token;
  size_t n = 0;
  ssize_t read;
  
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
    //printf("Chars read: %zu, Outputted line: %s", read, line);
    

    /* Word Tokenization & Storage */
    token = strtok(line, IFS);
    //size_t wordIndex = 0;
    //int enableBackgroundProcess = 0;
    while (token) {

      // Stops tokenizing if remaining text is commented with hash symbol.
      if (strncmp(token, "#", 1) == 0) break;

      // Stored Token
      printf("Storing token: %s\n", token);
      char *dupToken = strdup(token);
      // Add to array
      free(dupToken);

      token = strtok(NULL, IFS);
      if (!token) {
        // Last word occurences of "&" indicates that the command is to be run in the background. 
        //if (strcmp("&", "&") == 0) enableBackgroundProcess = 1;
        break;
      }
      //wordIndex++;
    }


    /* Parse commands */



    /* Execution & Built-In Commands */


    /* Execution & Non-Built-In Commands */



    /* Waiting & Signal Handling */


  };

  free(line);

  exit(EXIT_SUCCESS);
  
}

