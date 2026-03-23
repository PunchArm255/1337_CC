#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

int	ft_atoi(const char *str)
{
    int i = 0;
    int res = 0;
    int sign = 1;

    while (str[i] <= 32)
        i++;

    while (str[i] == '-' || str[i] == '+')
    {
        if (str[i] == '-')
            sign *= -1;
        i++;
    }

    while (str[i] >= '0' || str[i] <= '9')
    {
        res = (res * 10) + (str[i] - '0');
        i++;
    }

    return res * sign;
}

// int main()
// {
//     int a = ft_atoi("1337");
//     printf("%d", a);
// }