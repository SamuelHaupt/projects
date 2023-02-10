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
  
  char *ps1 = getenv("PS1");
  char *ifs = getenv("IFS") ? getenv("IFS") : " \t\n";
  char *line = NULL;
  char *str_token;
  size_t n = 0;
  ssize_t read;
  struct token_s *word_list = NULL;
  size_t word_count = 0;
  
  while (1) {
    
    /* Manage Background Processes */


    /* Prompt & Read Line of Input */
restart_prompt:
    fprintf(stderr, "%s", ps1);
    read = getline(&line, &n, stdin);
    if (read == -1) {
      err(errno, "getline error");
      goto restart_prompt;
    }
    
    if (1) {
      /* Replaces $$ with smallsh pid. Uses strstr to detect if
       * needle exists in haystack within str_gsub. */
      char *sub = {0};
      int converted = asprintf(&sub, "%jd", (intmax_t) getpid());
      if (converted == -1) {
        free(sub);
        goto restart_prompt;
      }
      
      char const *needle = "$$";
      char *gsub_return = str_gsub(&line, needle, sub);
      free(sub);
      if (!gsub_return) goto restart_prompt;
      line = gsub_return;
    }

    /* Word Tokenization & Storage */
    str_token = strtok(line, ifs);
    while (str_token) {

      // Stops tokenizing if remaining text is commented with hash symbol.
      if (strncmp(str_token, "#", 1) == 0) break;
      if (strcmp(str_token, "~/") == 0) {
        printf("here %jd", (intmax_t) getpid());
      }
      // Stored Token
      char *dup_token = strdup(str_token);
      // Add to array
      process_token(&word_list, &word_count, dup_token);
      printf("Stored token: %s at index %zu\n", str_token, word_count);
      free(dup_token);

      str_token = strtok(NULL, ifs);
      if (!str_token) {
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

