#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>

int		max(int* tab, unsigned int len)
{
    unsigned int i = 1;
    int max;

    if (len == 0)
        return 0;

    max = tab[0];

    while (i < len)
    {
        if (tab[i] > max)
            max = tab[i];
        i++;
    }
    return max;
}

int main()
{
    int tab[5] = {22, 101, 9, 56, 77};
    printf("%d\n", max(tab, 5));
}