//#define _POSIX_C_SOURCE 200809L
//#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>

/* Function prototype str_gsub provided by Ryan Gambord at Oregon State University Operating Systems Course */
extern char *str_gsub(char *restrict *restrict haystack, char const *restrict needle, char const *restrict sub);

extern void process_token(char *restrict *restrict wordList, size_t *restrict wordCount, char const *restrict dupToken);
