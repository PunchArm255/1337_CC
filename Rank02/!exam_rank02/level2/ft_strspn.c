#include <stdio.h>
#include <string.h>

size_t	ft_strspn(const char *s, const char *accept)
{
    size_t i = 0;
    size_t j;
    int found;

    while (s[i])
    {
        j = 0;
        found = 0;
        while (accept[j])
        {
            if (s[i] == accept[j])
                found = 1;
            j++;
        }
        if (found == 0)
            return i;
        i++;
    }
    return i;
}

// int main(int ac, char **av)
// {
//     printf("%zu\n", ft_strspn(av[1], av[2]));
//     printf("%zu\n", strspn(av[1], av[2]));
// }