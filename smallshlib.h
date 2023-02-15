//#define _POSIX_C_SOURCE 200809L
//#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>

typedef struct token_s {
  char *word;
  char *info;
} token_s;

/* Function prototype str_gsub provided by Ryan Gambord at Oregon State University Operating Systems Course */
extern char *str_gsub(char *restrict *restrict haystack, char const *restrict needle, char const *restrict sub);

extern void process_token(char **words, size_t *restrict word_count, char *restrict token);

extern void reset_token_array(char *restrict *restrict words, size_t *restrict word_count);

extern int str_to_int(char *restrict str);
