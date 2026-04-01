#include <stdio.h>
#include <stdlib.h>

int main(int ac, char **av)
{
    if (ac == 2)
    {
        int i = 2;
        int n = atoi(av[1]);

        if (n == 1)
            printf("1");

        while (n > 1)
        {
            if (n % i == 0)
            {
                printf("%d", i);
                if (n != i)
                    printf("*");
                n /= i;
            }
            else
                i++;
        }
    }
    printf("\n");
}