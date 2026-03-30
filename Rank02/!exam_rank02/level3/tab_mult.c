#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

void    ft_putchar(char c)
{
    write(1, &c, 1);
}

void    ft_putnbr(int nb)
{
    if (nb > 9)
    {
        ft_putnbr(nb / 10);
        ft_putnbr(nb % 10);
    }
    else
        ft_putchar(nb + '0');
}

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

int main(int ac, char **av)
{
    if (ac == 2)
    {
        int i = 1;
        int num = ft_atoi(av[1]);

        while (i < 10)
        {
            ft_putnbr(i);
            write(1, " x ", 3);
            ft_putnbr(num);
            write(1, " = ", 3);
            ft_putnbr(i*num);
            write(1, "\n", 1);
            i++;
        }
    }
    else
        write(1, "\n", 1);
}