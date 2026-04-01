#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main(int ac, char **av)
{
    if (ac == 3)
    {
        int num1 = atoi(av[1]);
        int num2 = atoi(av[2]);

        while (num1 > 0 && num2 > 0)
        {
            if (num1 > num2)
                num1 -= num2;
            else
                num2 -= num1;
        }

        printf("%d", num1);
    }
    printf("\n");
}