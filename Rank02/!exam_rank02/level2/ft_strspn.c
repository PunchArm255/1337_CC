#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

size_t	ft_strspn(const char *s, const char *accept)
{
    size_t i = 0; 
    size_t j = 0;
    int check;

    while (s[i])
    {
        while (accept[j])
        {
            if (s[i] == accept[j])
                check = 1;
            j++;
        }

        if (check == 0)
            return i;
        i++;
    }
}