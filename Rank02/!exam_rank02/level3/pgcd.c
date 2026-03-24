#include <stdio.h>
#include <stdlib.h>

int main(int ac, char **av)
{
    if (ac == 3)
    {
        int a = atoi(av[1]);
        int b = atoi(av[2]);

        if (a > 0 && b > 0)
        {
            while (a != b)
            {
                if (a > b)
                    a -= b;
                else
                    b -= a;
            }
            printf("%d", a);
        }
    }
    printf("\n");
}