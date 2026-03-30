#include <stdlib.h>
#include <stdio.h>

int     *ft_range(int start, int end)
{
    int len = (end - start) < 0 ? ((end - start) * -1) + 1 : (end - start) + 1;
    int i = 0;
    int *res;

    res = (int *)malloc(sizeof(int) * len);
    if (!res)
        return NULL;

    while (i < len)
    {
        if (start < end)
            res[i] = start++;
        else
            res[i] = start--;
        i++;
    }
    return res;
}

// int main()
// {
//     int i = 0;
//     int *tab = ft_range(-1, 2);

//     while (i < 4)
//     {
//         printf("%d, ", tab[i]);
//         i++;
//     }
// }