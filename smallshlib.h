#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>


extern char
*str_gsub(char *restrict *restrict haystack, char const *restrict needle, char const *restrict sub);


extern int
token_expansion(char *restrict *restrict haystack,
                      size_t words_count,
                      char *restrict exp_home, 
                      char *restrict exp_str_pid_smallsh, 
                      char *restrict exp_str_exit_status,
                      char *restrict exp_str_bg_pid);


extern void
process_token(char **words, size_t *restrict words_count, char *restrict token);


extern void
reset_token_array(char *restrict *restrict words, size_t *restrict words_count);


extern int
str_to_int(char *restrict str);


extern int
parse_commands(char *restrict *restrict words,
               size_t *restrict words_count,
               int *restrict bg_set_command,
               char *restrict *restrict in_file_pathname,
               char *restrict *restrict out_file_pathname);


extern void
handler_with_no_action(int signal);
