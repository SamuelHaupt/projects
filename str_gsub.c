#define _POSIX_C_SOURCE 200809L

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stddef.h>

/* Function prototype provided by Ryan Gambord at Oregon State University Operating Systems Course */
char *str_gsub(char *restrict *restrict haystack, char const *restrict needle, char const *restrict sub);

int main(int argc, char *argv[])
{
  if (argc != 3) exit(EXIT_FAILURE);
  char *line = NULL;
  size_t n = 0;
  getline(&line, &n, stdin);
  {
    char *return_value = str_gsub(&line, argv[1], argv[2]);
    if (!return_value) exit(EXIT_FAILURE);
    line = return_value;
  }

  printf("%s", line);
  free(line);

  return EXIT_SUCCESS;
}

/* Function prototype provided by Ryan Gambord at Oregon State University Operating Systems Course */
char *str_gsub(char *restrict *restrict haystack, char const *restrict needle, char const *restrict sub)
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
