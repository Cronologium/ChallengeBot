#include <stdlib.h>
#include <stdio.h>

//class Solution

typedef struct {
    char board[3][3];
    char playing;
} Api;

__attribute__((visibility("default"))) char* put(Api api, char** buffer)
{
    char* result = malloc(4);

    int i = 0;
    while (i < 9 && api.board[i / 3][i % 3] != ' ')
    {
        ++i;
    }
    --i;
    result[0] = (char)((i / 3) + '0');
    result[1] = ' ';
    result[2] = (char)((i % 3) + '0');
    result[3] = 0;
    *buffer = result;
}