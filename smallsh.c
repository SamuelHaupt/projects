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
#include <signal.h>
#include <string.h>
#include "smallshlib.h"

#define WORD_LIMIT 512

static void
handler_with_no_action(int signal)
{
}

int
main(void)
{
  
  char *PS1 = getenv("PS1") ? getenv("PS1") : "" ;
  char *IFS = getenv("IFS") ? getenv("IFS") : " \t\n";
  char *line = 0;
  char *str_token = 0;
  size_t n = 0;
  size_t read; 
  char **words;
  words = calloc(WORD_LIMIT, sizeof **words);
  size_t words_count = 0;
  pid_t w_pid = 0;
  pid_t bg_child_pid;
  int bg_child_process;
  struct sigaction  sa_SIGINT_default = {0}, 
                    sa_SIGINT_do_nothing = {0},
                    sa_SIGINT_old = {0},
                    sa_SIGINT_ignore = {0},
                    sa_SIGTSTP_default = {0},
                    sa_ignore = {0};

  sa_SIGINT_do_nothing.sa_handler = handler_with_no_action;
  sa_ignore.sa_handler = SIG_IGN;
  /* Ignore job-control stop signal (Control-Z). */
  sigaction(SIGTSTP, &sa_ignore, &sa_SIGTSTP_default);
  /* Ignore terminal interrupt signal (Control-C). */
  sigaction(SIGINT, &sa_ignore, &sa_SIGINT_default);
  
restart_prompt:
  while (1) {
    /* Manage Background Processes */
    while ((bg_child_pid = waitpid(0, &bg_child_process, WUNTRACED | WNOHANG)) > 0) {
      if (WIFEXITED(bg_child_process)){
        fprintf(stderr, "Child process %d done. Exit status %d.\n", bg_child_pid, WEXITSTATUS(bg_child_process));
      } else if (WIFSIGNALED(bg_child_process)) {
        fprintf(stderr, "Child process %d done. Signaled %d.\n", bg_child_pid, WTERMSIG(bg_child_process));
      } else if (WIFSTOPPED(bg_child_process)) {
        if (kill(bg_child_pid, SIGCONT) == -1) err(errno, "kill");
        fprintf(stderr, "Child process %d stopped. Continuing.\n", bg_child_pid);
      }
    }
    if (bg_child_pid == -1 && errno != ECHILD) err(errno, "waitpid");

    /* Prompt & Read Line of Input */

    fprintf(stderr, "%s", PS1);
    if (sigaction(SIGINT, &sa_SIGINT_do_nothing, &sa_SIGINT_old) == -1) err(errno, "sigaction set to current");
    read = getline(&line, &n, stdin);
    if (sigaction(SIGINT, &sa_SIGINT_old, NULL) == -1) err(errno, "sigaction set to old");
    if (read == 1) continue; // No input except newline character. Skip strtok below.
    if (read == -1) {
      fprintf(stderr, "\n"); // Adds new line when interrupt signal is sent.
      if (feof(stdin)) goto exit;
      if (errno == EINTR) {
        clearerr(stdin);
        errno = 0;
        continue;
      }
    }
    
    //if (0) {
      /* Replaces $$ with smallsh pid. Uses strstr to detect if
       * needle exists in haystack within str_gsub. */
      //char *sub = {0};
      //int converted = asprintf(&sub, "%jd", (intmax_t) getpid());
      //if (converted == -1) {
        //free(sub);
        //goto restart_prompt;
      //}
      
      //char const *needle = "$$";
      //char *gsub_return = str_gsub(&line, needle, sub);
      //free(sub);
      //if (!gsub_return) goto restart_prompt;
      //line = gsub_return;
    //}

    /* Word Tokenization & Storage */
    str_token = strtok(line, IFS);
    while (str_token && words_count < WORD_LIMIT) {

      // Stops tokenizing if remaining text is commented with hash symbol.
      if (strncmp(str_token, "#", 1) == 0) break;
      if (strcmp(str_token, "~/") == 0) {
        printf("here %jd", (intmax_t) getpid());
      }
      // Stored Token
      char *dup_token = strdup(str_token);
      // Add to array
      process_token(words, &words_count, dup_token);
      str_token = strtok(NULL, IFS);
      if (!str_token) {
        break;
      } 
    }
    
    // fd = open()
    // dup2(fd, STDOUT_FILENO)
    // close(fd)

    /* Parse commands */



    /* Execution & Built-In Commands */

    if (words_count == 1 && strcmp(words[0], "exit") == 0) { 
      goto exit;
    }
    // if (strcmp(words[0], "cd") == 0) {
    //   if (words_count == 1) chdir(getenv("HOME"));
    //   if (words_count == 2) chdir(words[1]);
    //   if (words_count > 2) err(errno, "cd command");
    //   reset_token_array(words, &words_count);
    //   goto restart_prompt;
    // }
    
    /* Adopted from Linux Programming Interface Chapter 25. */
    switch (w_pid = fork()) {
      case -1:
        /* Handle error. */
        err(errno, "fork");
        break;
      case 0:
        /* Perform actions specific to child. */
        /* Execution & Non-Built-In Commands */
        if (sigaction(SIGTSTP, &sa_SIGTSTP_default, NULL) == -1) err(errno, "SIGTSTOP not set to default");
        if (sigaction(SIGINT, &sa_SIGINT_default, NULL) == -1) err(errno, "SIGINT not set to default");
        execvp(words[0], words);
        fprintf(stderr, "execvp: %s\n", strerror(errno));
        _exit(errno);
        break;
      default:
        /* Perform actions specific to parent. */
        /* Waiting & Signal Handling */
        bg_child_pid = waitpid(w_pid, &bg_child_process, 0);
        if (bg_child_pid == -1) {
          err(errno, "waitpid");
        }

        if (strcmp(words[0], "cd") == 0) {
          if (words_count == 1) chdir(getenv("HOME"));
          if (words_count == 2) chdir(words[1]);
          if (words_count > 2) err(errno, "cd command");
          reset_token_array(words, &words_count);
          // goto restart_prompt;
        }
    }
    reset_token_array(words, &words_count);
  };

exit:
  reset_token_array(words, &words_count);
  free(words);
  if (line != 0) free(line);

  exit(EXIT_SUCCESS);
  
}

