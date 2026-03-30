#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>

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

int is_prime(int n)
{
    int i = 2;

    if (n < 2)
        return 0;

    while (i <= n / 2)
    {
        if (n % i == 0)
            return 0;
        i++;
    }
    return 1;
}

int main(int ac, char **av)
{
    if (ac == 2 && ft_atoi(av[1]) > 0)
    {
        int num = ft_atoi(av[1]);
        int sum = 0;

        while (num > 1)
        {
            if (is_prime(num))
                sum += num;
            num--;
        }
        ft_putnbr(sum);
        write(1, "\n", 1);
    }
    else
        write(1, "0\n", 2);
}