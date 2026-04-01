#include <stdio.h>
#include <stdlib.h>

int get_len(long n)
{
    int len = 0;

    if (n <= 0)
        len = 1;

    while (n != 0)
    {
        n = n / 10;
        len++;
    }
    return len;
}

char	*ft_itoa(int nbr)
{
    long n = nbr;
    int len = get_len(n);
    int i = 0;
    char *res = (char *)malloc(sizeof(char) * len + 1);
    if (!res)
        return NULL;

    res[len] = '\0';
    len--;

    if (n == 0)
        res[0] = '0';

    if (n < 0)
    {
        res[0] = '-';
        n *= -1;
    }

    while (n > 0)
    {
        res[len] = n % 10 + '0';
        n = n / 10;
        len--;
    }
    return res;
}

// int main(int ac, char **av)
// {
//     printf("%s\n", ft_itoa(atoi(av[1])));
// }