#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int ft_strlen(char *str)
{
    int i = 0;
    while (str[i])
        i++;
    return i;
}

char    *ft_strdup(char *src)
{
    int len = ft_strlen(src) + 1;
    int i = 0;
    char *dup;

    dup = (char *)malloc(sizeof(char) * len);
    if (!dup)
        return NULL;

    while (src[i])
    {
        dup[i] = src[i];
        i++;
    }

    dup[i] = '\0';
    return dup;
}

// int main(int ac, char **av)
// {
//     printf("%s\n", ft_strdup(av[1]));
//     printf("%s\n", strdup(av[1]));
// }