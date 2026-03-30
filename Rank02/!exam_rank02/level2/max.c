#include <stdlib.h>
#include <stdio.h>

int		max(int* tab, unsigned int len)
{
    int max = tab[0];
    unsigned int i = 1;

    while (i < len)
    {
        if (tab[i] > max)
            max = tab[i];
        i++;
    }
    return max;
}

// int main(int ac, char **av)
// {
//     int tab[] = {0, 8, 7, 4, 9};
//     printf("%d\n", max(tab, 5));
// }