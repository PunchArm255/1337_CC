#include <unistd.h>
#include <stdlib.h>

int     *ft_rrange(int start, int end)
{
    int i = 0;
    int *tab;
    int size = (end - start < 0) ? (((end - start) * 1) + 1) : ((end - start) + 1)

    tab = (int *)malloc(sizeof(int) * size);
    if (!tab)
        return NULL;
    
    while (i < size)
    {
        if (start < end)
            tab[i] = end--;
        else
            tab[i] = end++;
        i++;
    }

    return tab;
}