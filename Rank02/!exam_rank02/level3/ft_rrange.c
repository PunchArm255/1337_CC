#include <stdlib.h>
#include <stdio.h>

int     *ft_rrange(int start, int end)
{
    int i = 0;
    int len = (end - start) < 0 ? ((end - start) * -1) + 1 : (end - start) + 1;
    int *res;

    res = (int *)malloc(sizeof(int) * len);
    if (!res)
        return NULL;

    while (i < len)
    {
        if (start < end)
            res[i] = end--;
        else
            res[i] = end++;
        i++;
    }
    return res;
}

// int main()
// {
//     int i = 0;
//     int *tab = ft_rrange(-1, 2);

//     while (i < 4)
//     {
//         printf("%d, ", tab[i]);
//         i++;
//     }
// }