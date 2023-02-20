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


/* Adapted function from str_gsub authored by Ryan Gambord (Professor) at
* Oregon State University Operating Systems Course: February 2023.
*/
char 
*str_gsub(char *restrict *restrict haystack, char const *restrict needle, char const *restrict sub)
{
  char *str = *haystack;
  size_t haystack_len = strlen(str);
  size_t const needle_len = strlen(needle),
               sub_len = strlen(sub);

  for (; (str = strstr(str, needle));) {
    ptrdiff_t offset = str - *haystack;
    if (sub_len > needle_len) {
      str = realloc(*haystack, sizeof **haystack * (haystack_len + sub_len - needle_len + 1));
      if (!str) goto exit;
      *haystack = str;
      str = *haystack + offset;
    }
    memmove(str + sub_len, str + needle_len, haystack_len + 1 - offset - needle_len);
    memcpy(str, sub, sub_len);
    haystack_len = haystack_len + sub_len - needle_len;
    str += sub_len;
  }
  
  str = *haystack;
  if (sub_len < needle_len) {
    str = realloc(*haystack, sizeof **haystack * (haystack_len + 1));
    if (!str) goto exit;
    *haystack = str;
  }

exit:
  return str;
}


extern char
*token_expansion(char *restrict *restrict words, 
                      size_t words_count, 
                      char *restrict exp_str_home, 
                      char *restrict exp_str_pid_smallsh, 
                      char *restrict exp_str_exit_status, 
                      char *restrict exp_str_bg_pid)
{

  char const *HOME = "~/";
  char const *PID_SMALLSH = "$$";
  char const *EXIT_STATUS = "$?";
  char const *BG_PID = "$!";
  char *result = NULL;

  for (size_t w = 0; w < words_count; w++) {

    result = str_gsub(&words[w], HOME, exp_str_home);
    if (!result) {
      fprintf(stderr, "Error with expansion of ~/.");
      goto exit;
    }

    result = str_gsub(&words[w], PID_SMALLSH, exp_str_pid_smallsh);
    if (!result) {
      fprintf(stderr, "Error with expansion of $$.");
      goto exit;
    }

    result = str_gsub(&words[w], EXIT_STATUS, exp_str_exit_status);
    if (!result) {
      fprintf(stderr, "Error with expansion of $?.");
      goto exit;
    }

    result = str_gsub(&words[w], BG_PID, exp_str_bg_pid);
    if (!result) {
      fprintf(stderr, "Error with expansion of $!.");
      goto exit;
    }
  }

exit:
  return result;
}


extern void
process_token(char **words, size_t *restrict words_count, char *restrict token)
{
  (*words_count)++;
  words[(*words_count) - 1] = strdup(token);
  return;
}


extern void
reset_token_array(char *restrict *restrict words, size_t *restrict words_count)
{
  for (size_t i = 0; i < *words_count; ++i) {
      free(words[i]);
      words[i] = 0;
    }
  *words_count = 0;
}


extern int
str_to_int(char *restrict str_ptr)
{
  /*
  * Used source code in STRTOL(3) and adapted for use in smallsh.
  * Returns int status in the range from 0 to 255.
  * Otherwise: 
  *   Returns -1, if the entire status is not an int.
  *   Returns -2, if status is outside the contracted range.
  */
  int base = 10;
  char *end_ptr;
  long status;

  errno = 0;    /* To distinguish success/failure after call */
  status = strtol(str_ptr, &end_ptr, base);

  /* Check for various possible errors */
  if ((errno == ERANGE
      && (status == LONG_MAX || status == LONG_MIN))
      || (errno != 0 && status == 0)
      || (end_ptr == str_ptr)
      || (*end_ptr != '\0')) {
    return -1;
  }

  /* Check if status is within range. */
  if (status < 0 || status > 255) {
    return -2;
  } else {
    return (int) status;
  }
}


extern int
parse_commands(char *restrict *restrict words,
               size_t *restrict words_count,
               int *restrict bg_set_command,
               char *restrict *restrict in_file_pathname,
               char *restrict *restrict out_file_pathname)
{
  if (strcmp(words[*words_count - 1], "&") == 0){
    *bg_set_command = 1;
    words[*words_count-1] = NULL;
    (*words_count)--;
    if (*words_count == 0) {
      fprintf(stderr, "smallsh: parse error near '&'.\n");
      goto exit_failure;
    }
  }

  for(int i = 0; *words_count >= 2 && i < 2; i++) {
    if (strcmp(words[*words_count - 2], ">") == 0) {
      *out_file_pathname = words[*words_count - 1];
      free(words[*words_count-2]);
      words[*words_count-2] = NULL;
      *words_count -= 2;
    } else if (strcmp(words[*words_count - 2], "<") == 0) {
      *in_file_pathname = words[*words_count - 1];
      free(words[*words_count-2]);
      words[*words_count-2] = NULL;
      *words_count -= 2;
    }
  }
  return 0;

exit_failure:
  return -1;
}


extern void
handler_with_no_action(int signal)
{
}
