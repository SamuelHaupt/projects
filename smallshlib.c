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
extern char *str_gsub(char *restrict *restrict haystack, char const *restrict needle, char const *restrict sub)
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
