#include <unistd.h>
#include <stdlib.h>

void ft_putchar(char c)
{
    write(1, &c, 1);
}

int ft_atoi(char *str)
{
    int i = 0;
    int res = 0;

    while (str[i] <= 32)
        i++;
    
    while (str[i] >= '0' && str[i] <= '9')
    {
        res = (res * 10) + (str[i] - '0');
        i++;
    }

    return (res);
}

void ft_putnbr(int nb)
{
    if (nb > 9)
    {
        ft_putnbr(nb / 10);
        ft_putnbr(nb % 10);
    }
    else
        ft_putchar(nb + '0');
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
            ft_putnbr(i * num);
            write(1, "\n", 1);
            i++;
        }
    }
    else
        write(1, "\n", 1);
}