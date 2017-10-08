#include <stdio.h>


char[][5] ships = {"0 0 0 4", "1 0 1 3", "3 0 3 2", "4 0 4 2", "6 0 6 1"};

int main() {
    int i = 0;
    int size;
    for (i = 0; i < 5; ++i)
    {
        scanf("%d", &size);
        printf("%s\n", ships[i]);
    }
    return 0;
}