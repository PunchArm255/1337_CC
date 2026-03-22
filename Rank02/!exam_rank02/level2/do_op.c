#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

int main(int ac, char **av)
{
    if (ac == 4)
    {
        int i = 0;
        int res;
        int num1 = atoi(av[1]);
        int num2 = atoi(av[3]);

        if (av[2][0] == '+')
            res = num1 + num2;
        else if (av[2][0] == '*')
            res = num1 * num2;
        else if (av[2][0] == '-')
            res = num1 - num2;
        else if (av[2][0] == '/')
            res = num1 / num2;
        else if (av[2][0] == '%')
            res = num1 % num2;
        printf("%d", res);
    }
    printf("\n");
}