#include <unistd.h>
#include <stdlib.h>

int     *ft_range(int start, int end)
{
    int i = 0;
    int size = (end - start < 0) ? (((end - start) * -1) + 1) : (end - start) + 1;
    int *tab;

    tab = (int *)malloc(sizeof(int) * size);
    if (!tab)
        return 0;

    while (i < size)
    {
        if (start < end)
            tab[i] = start++;
        else
            tab[i] = start--;
        i++;
    }

    return tab;
}