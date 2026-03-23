#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>



int	ft_atoi_base(const char *str, int str_base)
{
    int i = 0;
    int res = 0;
    int sign = 1;
    int digit;

    while (str[i] <= 32)
        i++;

    if (str[i] == '-' || str[i] == '+')
    {
        if (str[i] == '-')
            sign *= -1;
        i++;
    }


    while (str[i])
    {
        if (str[i] >= '0' && str[i]<= '9')
            digit = (str[i] - '0');
        else if (str[i] >= 'a' && str[i] <= 'z')
            digit = (str[i] - 'a' + 10);
        else if (str[i] >= 'A' && str[i] <= 'Z')
            digit = (str[i] - 'A' + 10);
        else
            break;

        if (digit >= str_base)
            break;
        res = (res * str_base) + (digit);
        i++;
    }

    return (res * sign);
}

int main()
{
    printf("%d\n", ft_atoi_base("011", 2));
}
