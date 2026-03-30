#include <unistd.h>
#include <stdlib.h>

int	ft_atoi(const char *str)
{
    int i = 0;
    int sign = 1;
    int res = 0;

    while ((str[i] >= '\t' && str[i] <= '\r') || str[i] == ' ')
        i++;

    if (str[i] == '-' || str[i] == '+')
    {
        if (str[i] == '-')
            sign *= -1;
        i++;
    }

    while (str[i] >= '0' && str[i] <= '9')
    {
        res = (res * 10) + (str[i] - '0');
        i++;
    }

    return res*sign;
}

void    ft_putchar(char c)
{
    write(1, &c, 1);
}

void    ft_puthex(int nb)
{
    char *base = "0123456789abcdef";

    if (nb > 15)
    {
        ft_puthex(nb / 16);
        ft_puthex(nb % 16);
    }
    else
        ft_putchar(base[nb]);
}

int main(int ac, char **av)
{
    if (ac == 2)
    {
        int num = ft_atoi(av[1]);
        ft_puthex(num);
    }
    write(1, "\n", 1);
}