#include <unistd.h>
#include <stdlib.h>


void    ft_putchar(char c)
{
    write(1, &c, 1);
}

int ft_atoi(char *str)
{
    int i = 0;
    int res = 0;

    while (str[i] <= 32)
        i++;
    
    while (str[i])
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
    {
        ft_putchar(nb + '0');
    }
}

int is_prime(int nb)
{
    if (nb < 2)
        return 0;
    
    int i = 2;
    while (i * i <= 2)
    {
        if (nb % i == 0)
            return 0;
        i++;
    }
    return 1;
}


int main(int ac, char **av)
{
    int i = 0;
    int n;
    int sum = 0;

    if (ac == 2)
    {
        n = ft_atoi(av[1]);
        while (n > 1)
        {
            if (is_prime(n))
                sum += n;
            n--;
        }
        ft_putnbr(sum);
    }
    else
    {
        write(1, "0", 1);
    }
    write (1, "\n", 1);
}