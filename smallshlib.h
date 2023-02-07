//#define _POSIX_C_SOURCE 200809L                                                                                                                                 
//#define _GNU_SOURCE                                                                                                                                             
                                                                                                                                                                 
#include <stdio.h>                                                                                                                                              
#include <stdlib.h>                                                                                                                                             
#include <sys/types.h>

extern void process_token(char *restrict *restrict wordList, size_t *restrict wordCount, char const *restrict dupToken);

