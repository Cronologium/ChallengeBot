#include <stdlib.h>
#include <stdio.h>

typedef struct {
    char* my_board[10][10];
    char* their_board[10][10];
    int next_ship_size;
} Api;

int ships = 0;
int i = 0;
int j = 0;

void copy2(char* buffer, int x, int y) {
    buffer[0] = (char)(x + '0');
    buffer[2] = (char)(y + '0');
}

void copy(char* buffer, int x, int y, int z, int w) {
    buffer[0] = (char)(x + '0');
    buffer[2] = (char)(y + '0');
    buffer[4] = (char)(z + '0');
    buffer[6] = (char)(w + '0');
}

__attribute__((visibility("default"))) char* put(Api api, char** buffer)
{
    char* result = malloc(8); // "x y z t\0";
    result[1] = result[3] = result[5] = ' ';
    result[7] = '\0';
    if (ships == 0) //size 2
    {
        copy(result, 0, 0, 0, 1);
    }
    if (ships == 1) //size 3
    {
        copy(result, 1, 0, 1, 2);
    }
    if (ships == 2)
    {
        copy(result, 2, 0, 2, 2);
    }
    if (ships == 3) //size 4
    {
        copy(result, 3, 0, 3, 3);
    }
    if (ships == 4) // size 5
    {
        copy(result, 4, 0, 4, 4);
    }
    ships++;
    *buffer = result;
}

__attribute__((visibility("default"))) char* shoot(Api api, char** buffer)
{
    char* result = malloc(4);//"x y";
    result[1] = ' ';
    result[3] = '\0';
    copy2(result, i, j);
    if (j == 9)
    {
        j = -1;
        ++i;
    }
    ++j;
    *buffer = result;
}