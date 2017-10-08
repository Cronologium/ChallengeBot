#include <stdio.h>

int main() {
    char playing;
    int i;
    scanf("%c", &playing);
    if (playing == 'X')
    {
        for (i = 0; i < 5; ++i)
        {
            int x, y;
            printf("%d %d\n", (i * 2) / 3, (i * 2) % 3);
            fflush(stdout);
            scanf("%d %d", &x, &y);
        }
    } else {
        for (i = 0; i < 4; ++i)
        {
            int x, y;
            scanf("%d %d", &x, &y);
            printf("%d %d\n", ((i * 2) + 1) / 3, ((i * 2) + 1) % 3);
            fflush(stdout);
        }
    }
    return 0;
}