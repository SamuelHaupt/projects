#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>

typedef struct token_s {
  char *word;
  char *info;
} token_s;

/* Function prototype str_gsub provided by Ryan Gambord at Oregon State University Operating Systems Course */
extern char *str_gsub(char *restrict *restrict haystack,
                      size_t words_count,
                      char *restrict exp_home, 
                      char *restrict exp_str_pid_smallsh, 
                      char *restrict exp_str_exit_status,
                      char *restrict exp_str_bg_pid);

extern void process_token(char **words, size_t *restrict word_count, char *restrict token);

extern void reset_token_array(char *restrict *restrict words, size_t *restrict word_count);

extern int str_to_int(char *restrict str);

extern void handler_with_no_action(int signal);
