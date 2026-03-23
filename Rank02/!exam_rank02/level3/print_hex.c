#include <unistd.h>
#include <stdlib.h>

// void    ft_putchar(char c)
// {
//     write(1, &c, 1);
// }

// void    ft_putnbr(int nb)
// {
//     if (nb > 9)
//     {
//         ft_putnbr(nb / 10);
//         ft_putnbr(nb % 10);
//     }
//     else
//     {
//         ft_putchar(nb + '0');
//     }
// }

// int main(int ac, char **av)
// {
//     if (ac == 2)
//     {
//         int i = 0;
//         int res = 0;

//         while (av[1][i])
//         {
//             res = (res * 16) + (av[1][i] - 'a' + 10);
//             i++;
//         }
//         ft_putnbr(res);
//     }
//     write(1, "\n", 1);
// }