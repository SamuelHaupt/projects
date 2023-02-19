#define _POSIX_C_SOURCE 200809L
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


int
main(void)
{
  /* ******************* */
  /* Signal Manipulation */
  /* ******************* */
  struct sigaction  sa_SIGINT_default = {0}, // (Ctrl-c) job control for stop
                    sa_SIGINT_do_nothing = {0},
                    sa_SIGTSTP_default = {0}, // (Ctrl-z) interrupt
                    sa_ignore = {0};
  sa_SIGINT_do_nothing.sa_handler = handler_with_no_action;
  sa_ignore.sa_handler = SIG_IGN;
  sigaction(SIGINT, &sa_ignore, &sa_SIGINT_default);
  sigaction(SIGTSTP, &sa_ignore, &sa_SIGTSTP_default);

  
  /* ********************* */
  /* Environment variables */
  /* ********************* */
  char const *ps1 = getenv("PS1") ? getenv("PS1") : "";
  char const *ifs = getenv("IFS") ? getenv("IFS") : " \t\n";
  char *home = getenv("HOME") ? getenv("HOME") : "";


  /* ************************ */
  /* Expanded token variables */
  /* ************************ */
  // Variable expansion of "$$": process ID of smallsh process.
  char exp_str_pid_smallsh[11] = {0};
  if (sprintf(exp_str_pid_smallsh, "%jd", (intmax_t) getpid()) <= 0) err(errno=EOVERFLOW, "exp_str_pid_smallsh");

  // Variable expansion of "$?": exit status of last foreground command.
  int exp_int_fg_exit_status = 0;

  // Variable expansion of "$!": process ID of most recent background process.
  char exp_str_bg_pid[8] = {0};


  /* *********************** */
  /* Miscellaneous variables */
  /* *********************** */
  // Getline variables
  size_t words_count = 0;
  char **words = malloc(sizeof **words * (WORD_LIMIT + 1));
  char *line = 0;
  char *str_token = 0;
  size_t n = 0;
  size_t read;

  // Parse, Fork, & Wait variables
  char *in_file = NULL;
  char *out_file = NULL;
  pid_t pid_bg_child = 0;
  int int_bg_child_status;
  int bg_set_command = 0;


  /* ************** */
  /* smallsh Access */
  /**************** */
  while (1) {
    home = getenv("HOME") ? getenv("HOME") : "";


    /* *************************** */
    /* Manage Background Processes */
    /* *************************** */
    while ((pid_bg_child = waitpid(0, &int_bg_child_status, WUNTRACED | WNOHANG)) > 0) {
      if (WIFEXITED(int_bg_child_status)){
        fprintf(stderr, "Child process %d done. Exit status %d.\n", pid_bg_child, WEXITSTATUS(int_bg_child_status));
      } else if (WIFSIGNALED(int_bg_child_status)) {
        fprintf(stderr, "Child process %d done. Signaled %d.\n", pid_bg_child, WTERMSIG(int_bg_child_status));
      } else if (WIFSTOPPED(int_bg_child_status)) {
        exp_int_fg_exit_status = pid_bg_child;
        if (kill(pid_bg_child, SIGCONT) == -1) err(errno, "kill");
        fprintf(stderr, "Child process %d stopped. Continuing.\n", pid_bg_child);
      }
    }
    if (pid_bg_child == -1 && errno != ECHILD) err(errno, "waitpid");
    

    /* ************************* */
    /* Print Prompt & Read Input */
    /* ************************* */
    fprintf(stderr, "%s", ps1);
    if (sigaction(SIGINT, &sa_SIGINT_do_nothing, NULL) == -1) err(errno, "sigaction set to current");
    read = getline(&line, &n, stdin);
    if (sigaction(SIGINT, &sa_ignore, NULL) == -1) err(errno, "sigaction set to old");
    if (read == 1) continue; // No input except newline character. Skip strtok below.
    if (read == -1) {
      fprintf(stderr, "\n"); // Adds new line when interrupt signal is sent.
      if (feof(stdin)) exit(exp_int_fg_exit_status); // Implied exit when EOF.
      if (errno == EINTR) {
        clearerr(stdin);
        errno = 0;
        continue;
      }
    }
    

    /* *************************** */
    /* Word Tokenization & Storage */
    /* *************************** */
    {  
      str_token = strtok(line, ifs);
      if (str_token) {
        goto start_tokenization;
      } else {
        goto restart_prompt;
      }

      char *dynamic_token = NULL;
      while ((str_token = strtok(NULL, ifs)) != NULL && words_count < WORD_LIMIT) {
      start_tokenization:
        if (strncmp(str_token, "#", 1) == 0) break;
        dynamic_token = strdup(str_token);
        process_token(words, &words_count, dynamic_token);
      }
      free(dynamic_token);
      dynamic_token = NULL;
      
      /* Null terminate end of list for EXECVP. */
      free(words[words_count]);
      words[words_count] = NULL;
    }


    /* *************** */
    /* Token Expansion */
    /* *************** */
    {
      int length = snprintf(0, 0, "%d", exp_int_fg_exit_status);
      char *exp_str_exit_status = malloc(sizeof *exp_str_exit_status * (length + 1));
      if (snprintf(exp_str_exit_status, length + 1, "%d", exp_int_fg_exit_status) <= 0) err(errno=EOVERFLOW, "exp_str_exit_status");

      length = snprintf(0, 0, "%s%s", home, "/");
      char *exp_str_home = malloc(sizeof *exp_str_home * (length + 1));
      if (snprintf(exp_str_home, length + 1, "%s%s", home, "/") <= 0) err(errno=EOVERFLOW, "exp_str_home");
      
      char *result = token_expansion(words, words_count, exp_str_home, exp_str_pid_smallsh, exp_str_exit_status, exp_str_bg_pid);
      
      free(exp_str_exit_status);
      free(exp_str_home);
      
      if (!result) {
        fprintf(stderr, "Error with token expansion.");
        goto restart_prompt;
      }
    }


    /* ************** */
    /* Parse Commands */
    /* ************** */
    if (parse_commands(words, &words_count, &bg_set_command, &in_file, &out_file) == -1) goto restart_prompt;
    if (words_count == 0) goto restart_prompt;

    // fd = open()
    // dup2(fd, STDOUT_FILENO)
    // close(fd)


    /* ************************** */
    /* Built-in Command Execution */
    /* ************************** */
    if (words_count > 0 && strcmp(words[0], "exit") == 0) {
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
        reset_token_array(words, &words_count);
        free(line);
        exit(val); // Add implied exit if second argument is passed.
      } else {
        fprintf(stderr, "\nexit\n");
        if (kill(-(intmax_t) getpid(), SIGINT) == -1) fprintf(stderr, "Unable to kill with SIGINT: %s\n", strerror(errno));
        reset_token_array(words, &words_count);
        free(line);
        exit(EXIT_SUCCESS);
      }
    }

    if (words_count > 0 && strcmp(words[0], "cd") == 0) {
      if (words_count == 1) chdir(home);
      if (words_count == 2) chdir(words[1]);
      if (words_count > 2) err(errno, "cd command");
      goto restart_prompt;
    }

    goto restart_prompt; //// For testing purposes only.
    /* ****************************** */
    /* Non-Built-in Command Execution */
    /* ****************************** */
    /* Adopted from Linux Programming Interface Chapter 25. */
    pid_bg_child = fork();
    switch (pid_bg_child) {
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
        exp_int_fg_exit_status = 128 + WTERMSIG(int_bg_child_status);
        fprintf(stderr, "smallsh: command not found: %s\n", words[0]);
        exit(errno);
        break;
      default:
        /* Perform actions specific to parent. */
        /* Waiting & Signal Handling */
        pid_bg_child = waitpid(pid_bg_child, &int_bg_child_status, 0);
        if (pid_bg_child == -1) {
          err(errno, "waitpid");
        }
        exp_int_fg_exit_status = WEXITSTATUS(int_bg_child_status);
    }
restart_prompt:
  reset_token_array(words, &words_count);
  };

exit:
  reset_token_array(words, &words_count);
  if (line != 0) free(line);

  exit(EXIT_SUCCESS);
  
}

