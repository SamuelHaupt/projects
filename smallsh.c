//#define _POSIX_C_SOURCE 200809L
//#define _XOPEN_SOURCE 700
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
  
  char *PS1 = getenv("PS1") ? getenv("PS1") : "" ;
  char *IFS = getenv("IFS") ? getenv("IFS") : " \t\n";
  char *line = NULL;
  char *str_token;
  size_t n = 0;
  ssize_t read; 
  token_s *word_array = NULL;
  size_t word_count = 0;
  
  while (1) {
    
    /* Manage Background Processes */


    /* Prompt & Read Line of Input */
restart_prompt:
    fprintf(stderr, "%s", PS1);
    read = getline(&line, &n, stdin);
    if (read == -1) {
      err(errno, "getline error");
      goto restart_prompt;
    }
    
    //if (0) {
      /* Replaces $$ with smallsh pid. Uses strstr to detect if
       * needle exists in haystack within str_gsub. */
      //char *sub = {0};
      //int converted = asprintf(&sub, "%jd", (intmax_t) getpid());
      //if (converted == -1) {
        //free(sub);
        //goto restart_prompt;
      //}
      
      //char const *needle = "$$";
      //char *gsub_return = str_gsub(&line, needle, sub);
      //free(sub);
      //if (!gsub_return) goto restart_prompt;
      //line = gsub_return;
    //}

    /* Word Tokenization & Storage */
    str_token = strtok(line, IFS);
    while (str_token) {

      // Stops tokenizing if remaining text is commented with hash symbol.
      if (strncmp(str_token, "#", 1) == 0) break;
      if (strcmp(str_token, "~/") == 0) {
        printf("here %jd", (intmax_t) getpid());
      }
      // Stored Token
      char *dup_token = strdup(str_token);
      // Add to array
      printf("Stored token: %s at index %zu\n", str_token, word_count);
      process_token(&word_array, &word_count, dup_token);
      free(dup_token);

      str_token = strtok(NULL, IFS);
      if (!str_token) {
        break;
      } 
    }
    




    /* Parse commands */



    /* Execution & Built-In Commands */

    if (word_count == 1 && strcmp(word_array[0].word, "exit") == 0) { 
      exit(EXIT_SUCCESS);
    }
    if (strcmp(word_array[0].word, "cd") == 0) {
      if (word_count == 1) chdir(getenv("HOME"));
      if (word_count == 2) chdir(word_array[1].word);
      if (word_count > 2) err(errno, "cd command");
      goto restart_prompt;
    }
    
    /* Adopted from Linux Programming Interface Chapter 25. */
    pid_t child_pid;
    switch (child_pid = fork()) {
      case -1:
        /* Handle error. */
        
        break;
      case 0:
        /* Perform actions specific to child. */
        char const *dup[] = strdup(word_array[1].word);
        execvp(word_array[0].word, dup);

        break;
      default:
        /* Perform actions specific to parent. */
        

        break;
    }

    /* Execution & Non-Built-In Commands */



    /* Waiting & Signal Handling */

    reset_token_array(&word_array, &word_count);
  };

  free(word_array);
  free(line);

  exit(EXIT_SUCCESS);
  
}

