/*
NAME
  smallsh - basic shell written in c
SYNOPSIS
  make && PS1='$ ' ./smallsh
DESCRIPTION
  smallsh (small shell) is a command-line interface, similar to bash. It can handle general inputs.
AUTHOR
  Samuel haupt
NOTES
  - Use makefile by running 'make' command to compile for use. Use 'make debug' if creating a debug symbol table
  with -g flag.
  - PS1 defaults to an empty string. It'll be important to set the environment variable (PS1='$ ')so a
  prompt will print each time.
  - IFS daults to " \t\n". It is possible to remove spaces from delimitors (IFS=$'\t'$'\n') and smallsh will
  still work for <tabs><newlines>, which requires tabes for spaces.
  - Expansion: ~/, $$, $?, and $! all expand to respectively: home directory, process ID of smallsh process,
  exit status of last foreground command, and process ID of most recent background process.
  - Comments: Comments denoted by "# comments" or "#comments" are deleted.
  - Redirection: Use the input redirection operator "<" and/or output redirection operator ">" followed by 
  filepaths (any order) to redirect standard input or output. Redirection must be the final commands, not 
  withstanding &, which will be removed prior to processing redirection.
  - Background Process: Use "&" as the final command in order to send an executed command to the background
  process. smallsh prompt will continue immediately.
*/


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
#include <sys/stat.h>
#include <signal.h>
#include <string.h>
#include <fcntl.h>
#include "smallshlib.h"

#define WORD_LIMIT 512


int
main(void)
{
  /* ******************* */
  /* Signal Manipulation */
  /* ******************* */
  struct sigaction  sa_SIGINT_default = {0}, // (Ctrl-c) interrupt
                    sa_SIGINT_do_nothing = {0},
                    sa_SIGTSTP_default = {0}, // (Ctrl-z) stop
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
  char const *home = getenv("HOME") ? getenv("HOME") : "";


  /* ************************ */
  /* Expanded token variables */
  /* ************************ */
  // Variable expansion of "~/": home directory.
  // ~/ ---> home
  
  // Variable expansion of "$$": process ID of smallsh process.
  char exp_str_pid_smallsh[12] = {0};
  if (sprintf(exp_str_pid_smallsh, "%jd", (intmax_t) getpid()) <= 0) fprintf(stderr, "sprintf: %s", strerror(EOVERFLOW));

  // Variable expansion of "$?": exit status of last foreground command.
  int exp_int_fg_exit_status = 0;

  // Variable expansion of "$!": process ID of most recent background process.
  char exp_str_bg_pid[12] = {0};


  /* *********************** */
  /* Miscellaneous variables */
  /* *********************** */
  // Getline variables
  size_t words_count = 0;
  char **words = malloc(sizeof **words * (WORD_LIMIT + 1));
  char *line = NULL;
  char *str_token = 0;
  size_t n = 0;
  size_t read;

  // Parse, Fork, & Wait variables
  char *infile_pathname = NULL;
  int fd_input = 0;
  char *outfile_pathname = NULL;
  int fd_output = 0;
  pid_t pid_bg_child = 0;
  int int_bg_child_status;
  int bg_set_command = 0;


  /* ************** */
  /* smallsh Access */
  /**************** */
  while (1) {


    /* *************************** */
    /* Manage Background Processes */
    /* *************************** */
    // Loop used for unwaited for background processes in same process group ID as smallsh.
    // See WAITPID(2) example for code structure. 
    // WNOHANG: return immediately if no child has exited.
    // WUNTRACED: Return if a child has stopped.
    while ((pid_bg_child = waitpid(0, &int_bg_child_status, WNOHANG | WUNTRACED)) > 0) {
      if (WIFEXITED(int_bg_child_status)){
        fprintf(stderr, "Child process %jd done. Exit status %d.\n", (intmax_t) pid_bg_child, WEXITSTATUS(int_bg_child_status));
      } else if (WIFSIGNALED(int_bg_child_status)) {
        fprintf(stderr, "Child process %jd done. Signaled %d.\n", (intmax_t) pid_bg_child, WTERMSIG(int_bg_child_status));
      } else if (WIFSTOPPED(int_bg_child_status)) {
        if (kill(pid_bg_child, SIGCONT) == -1) fprintf(stderr, "SIGCONT failed: %s", strerror(errno));
        fprintf(stderr, "Child process %jd stopped. Continuing.\n", (intmax_t) pid_bg_child);
      }
    }
    if (pid_bg_child == -1 && errno!=ECHILD) fprintf(stderr, "waitpid: %s", strerror(errno));
    

    /* ************************* */
    /* Print Prompt & Read Input */
    /* ************************* */
    fprintf(stderr, "%s", ps1);
    // Sigaction is set per assignment requirements.
    if (sigaction(SIGINT, &sa_SIGINT_do_nothing, NULL) == -1) fprintf(stderr, "SIGINT not set: %s", strerror(errno));
    n = 0;
    read = getline(&line, &n, stdin);
    if (sigaction(SIGINT, &sa_ignore, NULL) == -1) fprintf(stderr, "SIGINT not set: %s", strerror(errno));
    if (read == 1) continue; // No input except newline character. Skip strtok below.
    if (read == (size_t) -1) {
      // Error or EOF condition exists per GETLINE(3)
      fprintf(stderr, "\n");
      if (feof(stdin)) goto eof_exit;
      if (errno == EINTR) {
        clearerr(stdin);
        errno = 0;
        goto restart_prompt;
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
        goto restart_prompt; // No token exists, so restart prompt.
      }

      while ((str_token = strtok(NULL, ifs)) != NULL && words_count < WORD_LIMIT) {
      start_tokenization:
        if (strncmp(str_token, "#", 1) == 0) break; // Stop tokenization since only comments remain.
        char *dynamic_token = strdup(str_token);
        add_token(words, &words_count, dynamic_token);
        free(dynamic_token);
        dynamic_token = NULL;
      }
      
      /* Null terminate end of list for EXECVP. See EXEC(3) for reference. */
      words[words_count] = NULL;
    }


    /* *************** */
    /* Token Expansion */
    /* *************** */
    {
      // Converts exit status to character array.
      int length = snprintf(0, 0, "%d", exp_int_fg_exit_status);
      char *exp_str_exit_status = malloc(sizeof *exp_str_exit_status * (length + 1));
      if (snprintf(exp_str_exit_status, length + 1, "%d", exp_int_fg_exit_status) <= 0) fprintf(stderr, "snprintf: %s", strerror(EOVERFLOW));

      // Add "/" to home before expanding tokens.
      length = snprintf(0, 0, "%s%s", home, "/");
      char *exp_str_home = malloc(sizeof *exp_str_home * (length + 1));
      if (snprintf(exp_str_home, length + 1, "%s%s", home, "/") <= 0) fprintf(stderr, "snprintf: %s", strerror(EOVERFLOW));
      
      int result = token_expansion(words, words_count, exp_str_home, exp_str_pid_smallsh, exp_str_exit_status, exp_str_bg_pid);
      
      free(exp_str_exit_status);
      free(exp_str_home);
      
      if (result == -1) {
        fprintf(stderr, "Error with token expansion.");
        goto restart_prompt;
      }
    }


    /* ************** */
    /* Parse Commands */
    /* ************** */
    // Parses commands related to redirection and background process. See documentation notes.
    if (parse_commands(words, &words_count, &bg_set_command, &infile_pathname, &outfile_pathname) == -1) goto restart_prompt;
    if (words_count == 0) goto restart_prompt; // Only happens when no other words exist aside from redirection and background process.


    /* ************************** */
    /* Built-in Command Execution */
    /* ************************** */
    // Only exit from smallsh.
    // exit command with valid argument executes with argument. See str_to_int for valid argument.
    // Otherwise, exit command executed with exit status of last foreground command.
    if (strcmp(words[0], "exit") == 0) {
      if (words_count > 2) {    
        fprintf(stderr, "Too many arguments passed with exit command.\n");
        goto restart_prompt;
      } else if (words_count == 2) {
        int status = str_to_int(words[1]);
        if ( status < 0) {
          if (status == -1) fprintf(stderr, "Invalid argument passed with exit command.\n");
          if (status == -2) fprintf(stderr, "Exit status out of range: 0 to 255.\n");
          goto restart_prompt;
        }
        fprintf(stderr, "\nexit\n");
        if (kill(-(intmax_t) getpid(), SIGINT) == -1) fprintf(stderr, "Unable to kill with SIGINT: %s\n", strerror(errno));
        free(line);
        reset_token_array(words, &words_count);
        free(words);
        exit(status);
      } else {
        fprintf(stderr, "\nexit\n");
        if (kill(-(intmax_t) getpid(), SIGINT) == -1) fprintf(stderr, "Unable to kill with SIGINT: %s\n", strerror(errno));
      eof_exit:
        free(line);
        reset_token_array(words, &words_count);
        free(words);
        exit(exp_int_fg_exit_status);
      }
    }

    if (strcmp(words[0], "cd") == 0) {
      if (words_count == 1) chdir(home);
      if (words_count == 2) chdir(words[1]);
      if (words_count > 2) fprintf(stderr, "cd: too many arguments passed: %s\n", words[1]);
      goto restart_prompt;
    }


    /* ****************************** */
    /* Non-Built-in Command Execution */
    /* ****************************** */
    /* Adopted from Linux Programming Interface Chapter 25. */
    /* Creates parent and child processes. */
    pid_bg_child = fork();
    switch (pid_bg_child) {
      
      /* Handle error. */
      case -1:
        fprintf(stderr, "fork: %s", strerror(errno));
        goto restart_prompt;
        break;
      
      /* Perform actions specific to child. */
      case 0:
        if (infile_pathname) {
          int result = -1;
          fd_input = open(infile_pathname, O_RDONLY);
          if (fd_input == -1) fprintf(stderr, "%s: %s", strerror(errno), infile_pathname);
          result = dup2(fd_input, STDIN_FILENO);
          if (result == -1 ) fprintf(stderr, "file descriptor error: %s\n", infile_pathname);
          close(fd_input);
          free(infile_pathname);
          infile_pathname = NULL;
        }

        if (outfile_pathname) {
          int result = -1;
          fd_output = open(outfile_pathname, O_CREAT | O_WRONLY | O_TRUNC, S_IRWXU | S_IRWXG | S_IRWXO );
          if (fd_output == -1) fprintf(stderr, "%s: %s", strerror(errno), outfile_pathname);
          result = dup2(fd_output, STDOUT_FILENO);
          if (result == -1 ) fprintf(stderr, "file descriptor error: %s\n", outfile_pathname);
          close(fd_output);
          free(outfile_pathname);
          outfile_pathname = NULL;
        }

        if (sigaction(SIGTSTP, &sa_SIGTSTP_default, NULL) == -1)  fprintf(stderr, "SIGTSTOP not set to default: %s", strerror(errno));
        if (sigaction(SIGINT, &sa_SIGINT_default, NULL) == -1) fprintf(stderr, "SIGINT not set to default: %s", strerror(errno));
        execvp(words[0], words);  // excevp returns errno only on error.
        
        fprintf(stderr, "smallsh: command not found: %s\n", words[0]);
        free(line);
        reset_token_array(words, &words_count);
        free(words);
        exit(errno);
        break;
      
      /* Perform actions specific to parent. */
      default:
        if (infile_pathname) {
          free(infile_pathname);
          infile_pathname = NULL;
        }

        if (outfile_pathname) {
          free(outfile_pathname);
          outfile_pathname = NULL;
        }
        
        // Skips blocking wait if recent command was sent to background process.
        if (bg_set_command == 1) {
          bg_set_command = 0;
          if (sprintf(exp_str_bg_pid, "%jd", (intmax_t) pid_bg_child) <= 0) fprintf(stderr, "sprintf: %s", strerror(EOVERFLOW));
          goto restart_prompt;
        }

        // Loop used for foreground commands: blocking wait.
        // See WAITPID(2) example for code structure. 
        // WUNTRACED: Return if a child has stopped.
        while ((pid_bg_child = waitpid(pid_bg_child, &int_bg_child_status, WUNTRACED)) > 0) {
          if (WIFEXITED(int_bg_child_status)){
            exp_int_fg_exit_status = WEXITSTATUS(int_bg_child_status);
          } else if (WIFSIGNALED(int_bg_child_status)) {
            exp_int_fg_exit_status = 128 + WTERMSIG(int_bg_child_status);
          } else if (WIFSTOPPED(int_bg_child_status)) {
            if (sprintf(exp_str_bg_pid, "%jd", (intmax_t) pid_bg_child) <= 0) fprintf(stderr, "sprintf: %s", strerror(EOVERFLOW));
            if (kill(pid_bg_child, SIGCONT) == -1) fprintf(stderr, "SIGCONT failed: %s", strerror(errno));
            fprintf(stderr, "Child process %d stopped. Continuing.\n", pid_bg_child);
            break; // Moves signaled child process to background.
          }
        }
        if (pid_bg_child == -1 && errno!=ECHILD) fprintf(stderr, "waitpid: %s", strerror(errno));

    }
restart_prompt:
  free(line);
  line = NULL;
  reset_token_array(words, &words_count);
  };  
}
