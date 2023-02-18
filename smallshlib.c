#define _POSIX_C_SOURCE 200809L
#define _GNU_SOURCE

#include <err.h>
#include <errno.h>
#include <getopt.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <stdint.h>
#include <stddef.h>
#include <sys/wait.h>
#include <sys/types.h>
#include <string.h>
#include <limits.h>
#include "smallshlib.h"

#define arr_len(obj) (sizeof obj / sizeof *obj)

/* Function str_gsub provided by Ryan Gambord at Oregon State University Operating Systems Course */
extern char *str_gsub(char *restrict *restrict words, 
                      size_t words_count, 
                      char *restrict exp_str_home, 
                      char *restrict exp_str_pid_smallsh, 
                      char *restrict exp_str_exit_status, 
                      char *restrict exp_str_bg_pid)
{
  char *word = *words;
  size_t word_len = strlen(words[0]);
  char const *HOME = "~/";
  size_t const HOME_len = strlen(HOME);
  char const *PID_SMALLSH = "$$";
  size_t const PID_SMALLSH_len = strlen(PID_SMALLSH);
  // char const *EXIT_STATUS = "$?";
  // char const *BG_PID = "$!";

  size_t exp_home_len = strlen(exp_str_home);
  size_t exp_pid_smallsh_len = strlen(exp_str_pid_smallsh);
  // size_t exit_status_len = strlen(exp_str_exit_status);
  // size_t bg_pid_len = strlen(exp_str_bg_pid);

  for (size_t w = 0; w < words_count; w++) {
    
    /* Replaces "~/" with home directory. */
    word = words[w];
    printf("%s\n", word);
    if (strncmp(word, HOME, 2) == 0) {
      word_len = strlen(words[w]);
      char *str_ptr = word;
      ptrdiff_t offset = str_ptr - words[w];
      str_ptr = realloc(words[w], sizeof *words[w] * (word_len + 1 + exp_home_len - HOME_len + 1)); // Remove "~" and keep "/".
      if (!str_ptr) goto exit;
      words[w] = str_ptr;
      
      size_t size_of_move = word_len + 1 - offset - HOME_len + 1; // Remove "~" and keep "/".
      memmove(word + exp_home_len, word + HOME_len, size_of_move);
      char *token = strdup(exp_str_home);
      memcpy(word, token, exp_home_len);
      word_len = word_len + exp_home_len - HOME_len + 1;
      word += exp_home_len;
      free(token);
    }

    /* Replaces "$$" with process ID of smallsh process. */
    word = words[w];
    printf("%s\n", word);
    for (;(word = strstr(word, PID_SMALLSH));) {
      word_len = strlen(words[w]);
      char *str_ptr = word;
      ptrdiff_t offset = str_ptr - words[w];
      str_ptr = realloc(words[w], sizeof *words[w] * (word_len + 1 + exp_pid_smallsh_len - PID_SMALLSH_len));
      if (!str_ptr) goto exit;
      words[w] = str_ptr;
      
      size_t size_of_move = word_len + 1 - offset - PID_SMALLSH_len; // Remove "$$".
      memmove(word + exp_pid_smallsh_len, word + PID_SMALLSH_len, size_of_move);
      char *token = strdup(exp_str_pid_smallsh);
      memcpy(word, token, exp_pid_smallsh_len);
      word_len = word_len + exp_pid_smallsh_len - PID_SMALLSH_len;
      word += exp_pid_smallsh_len;
      free(token);
    }
    
    word = words[w];
    printf("%s\n", word);
  }

  //   ptrdiff_t offset = str - *haystack;
  //   if (sub_len > needle_len) {
  //     str = realloc(*haystack, sizeof **haystack * (haystack_len + sub_len - needle_len + 1));
  //     if (!str) goto exit;
  //     *haystack = str;
  //     str = *haystack + offset;
  //   }
  //   memmove(str + sub_len, str + needle_len, haystack_len + 1 - offset - needle_len);
  //   memcpy(str, sub, sub_len);
  //   haystack_len = haystack_len + sub_len - needle_len;
  //   str += sub_len;
  
  // str = *haystack;
  // if (sub_len < needle_len) {
  //   str = realloc(*haystack, sizeof **haystack * (haystack_len + 1));
  //   if (!str) goto exit;
  //   *haystack = str;
//   }

exit:
  return *words;
}

extern void process_token(char **words, size_t *restrict word_count, char *restrict token)
{
  ++(*word_count);
  words[(*word_count) - 1] = token;
  return;
}

extern void reset_token_array(char *restrict *restrict words, size_t *restrict word_count)
{
  for (size_t i = 0; i < *word_count; ++i) {
      free(words[i]);
      words[i] = 0;
    }
  *word_count = 0;
}

extern int str_to_int(char *restrict str)
{
  /*
  * Used source code in STRTOL(3) and adapted for use in smallsh.
  * @brief Returns a int value in the range from 0 to 255. 
  * If the entire value is not an int, returns -1.
  * If value is outside the contracted range, returns -2.
  */
  int base = 10;
  char *endptr;
  long val;

  errno = 0;    /* To distinguish success/failure after call */
  val = strtol(str, &endptr, base);

  /* Check for various possible errors */
  if ((errno == ERANGE
      && (val == LONG_MAX || val == LONG_MIN))
      || (errno != 0 && val == 0)
      || (endptr == str)
      || (*endptr != '\0')) {
    return -1;
  }

  /* Check if val is within range. */
  if (val < 0 || val > 255) {
    return -2;
  } else {
    return (int) val;
  }
}

extern void handler_with_no_action(int signal) {}
