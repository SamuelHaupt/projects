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
#include "smallshlib.h"

#define arr_len(obj) (sizeof obj / sizeof *obj)

struct token_s {
  char *word;
  char *info;
};

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

extern void process_token(token_s *restrict *restrict word_array, size_t *restrict word_count, char *restrict token)
{
  struct token_s *array = *word_array;

  ++(*word_count);
  array = realloc(*word_array, sizeof **word_array * *word_count);
  if (!array) return;
  *word_array = array;
  
  (*word_array)[(*word_count) - 1].word = strdup(token);
  return;
}
