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
  words = calloc(WORD_LIMIT+1, sizeof **words);
  size_t words_count = 0;
  static char proc_grp_pid[10];
  if (sprintf(proc_grp_pid, "%jd", (intmax_t) getpid()) == 0) err(errno=EOVERFLOW, "proc_grp_pid");
  pid_t wait_pid = 0;
  pid_t bg_child_pid;
  int bg_child_process;
  static int shell_command_previous_status = 0; // Expansion of "$?"
  struct sigaction  sa_SIGINT_default = {0}, 
                    sa_SIGINT_do_nothing = {0},
                    sa_SIGTSTP_default = {0},
                    sa_ignore = {0};

  sa_SIGINT_do_nothing.sa_handler = handler_with_no_action;
  sa_ignore.sa_handler = SIG_IGN;
  sigaction(SIGTSTP, &sa_ignore, &sa_SIGTSTP_default);  /* Ignore job-control stop signal (Control-Z). */
  sigaction(SIGINT, &sa_ignore, &sa_SIGINT_default);    /* Ignore terminal interrupt signal (Control-C). */
  
  while (1) {
    /* Manage Background Processes */
    while ((bg_child_pid = waitpid(0, &bg_child_process, WUNTRACED | WNOHANG)) > 0) {
      if (WIFEXITED(bg_child_process)){
        fprintf(stderr, "Child process %d done. Exit status %d.\n", bg_child_pid, WEXITSTATUS(bg_child_process));
      } else if (WIFSIGNALED(bg_child_process)) {
        fprintf(stderr, "Child process %d done. Signaled %d.\n", bg_child_pid, WTERMSIG(bg_child_process));
      } else if (WIFSTOPPED(bg_child_process)) {
        shell_command_previous_status = bg_child_pid;
        if (kill(bg_child_pid, SIGCONT) == -1) err(errno, "kill");
        fprintf(stderr, "Child process %d stopped. Continuing.\n", bg_child_pid);
      }
    }
    if (bg_child_pid == -1 && errno != ECHILD) err(errno, "waitpid");
    fprintf(stderr, "exit: %d\n", shell_command_previous_status);
    /* Prompt & Read Line of Input */

    fprintf(stderr, "%s", PS1);
    if (sigaction(SIGINT, &sa_SIGINT_do_nothing, NULL) == -1) err(errno, "sigaction set to current");
    read = getline(&line, &n, stdin);
    if (sigaction(SIGINT, &sa_ignore, NULL) == -1) err(errno, "sigaction set to old");
    if (read == 1) continue; // No input except newline character. Skip strtok below.
    if (read == -1) {
      fprintf(stderr, "\n"); // Adds new line when interrupt signal is sent.
      if (feof(stdin)) exit(shell_command_previous_status); // Implied exit if EOF.
      if (errno == EINTR) {
        clearerr(stdin);
        errno = 0;
        continue;
      }
    }
    
    /* Word Tokenization & Storage */
    str_token = strtok(line, IFS);
    while (str_token && words_count < WORD_LIMIT) {
      // printf("%s", str_token);
      // Stops tokenizing if remaining text is commented with hash symbol.
      if (strcmp(str_token, "~/") == 0) {
        printf("here %jd", (intmax_t) getpid());
      }
      // Stored Token
      char *dup_token = NULL;
      if (strncmp(str_token, "#", 1) > 0) {
        dup_token = strdup(str_token);
      }
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

    /* Execution & Built-In Commands */

    if (strcmp(words[0], "exit") == 0) {
      if (words_count > 2) {    
        fprintf(stderr, "Too many arguments passed with exit command.\n");
        goto restart_prompt;
      } else if (words_count == 2) {
        int val = str_to_int(words[1]);
        if ( val < 0) {
          if (val == -1) fprintf(stderr, "Invalid argument passed with exit command.\n");
          if (val == -2) fprintf(stderr, "Exit status out of range: 0 to 255.\n");
          goto restart_prompt;
        }
        fprintf(stderr, "\nexit\n");
        if (kill(-(intmax_t) getpid(), SIGINT) == -1) fprintf(stderr, "Unable to kill with SIGINT: %s\n", strerror(errno));
        exit(val); // Add implied exit if second argument is passed.
      } else {
        fprintf(stderr, "\nexit\n");
        if (kill(-(intmax_t) getpid(), SIGINT) == -1) fprintf(stderr, "Unable to kill with SIGINT: %s\n", strerror(errno));
        exit(EXIT_SUCCESS);
      }
    }

    if (strcmp(words[0], "cd") == 0) {
      if (words_count == 1) chdir(getenv("HOME"));
      if (words_count == 2) chdir(words[1]);
      if (words_count > 2) err(errno, "cd command");
      reset_token_array(words, &words_count);
      goto restart_prompt;
    }
    
    /* Adopted from Linux Programming Interface Chapter 25. */
    wait_pid = fork();
    switch (wait_pid) {
      case -1:
        /* Handle error. */
        err(errno, "fork");
        exit(errno);
        break;
      case 0:
        /* Perform actions specific to child. */
        /* Execution & Non-Built-In Commands */
        if (sigaction(SIGTSTP, &sa_SIGTSTP_default, NULL) == -1) err(errno, "SIGTSTOP not set to default");
        if (sigaction(SIGINT, &sa_SIGINT_default, NULL) == -1) err(errno, "SIGINT not set to default");
        execvp(words[0], words);
        shell_command_previous_status = 128 + WTERMSIG(bg_child_process);
        fprintf(stderr, "Command failed to execute: %s\n", strerror(errno));
        exit(errno);
        break;
      default:
        /* Perform actions specific to parent. */
        /* Waiting & Signal Handling */
        bg_child_pid = waitpid(wait_pid, &bg_child_process, 0);
        if (bg_child_pid == -1) {
          err(errno, "waitpid");
        }
        shell_command_previous_status = WEXITSTATUS(bg_child_process);
    }
restart_prompt:
  reset_token_array(words, &words_count);
  };

exit:
  reset_token_array(words, &words_count);
  free(words);
  // free(proc_grp_pid);
  if (line != 0) free(line);

  exit(EXIT_SUCCESS);
  
}

