#include <stdlib.h>
#include <unistd.h>

int main(int ac, char **av)
{
    if (ac == 2)
    {
        int i = 0;
        int j;

        while(av[1][i])
            i++;
        i--;

        while(av[1][i] <= 32)
            i--;

        while(av[1][i] > 32)
            i--;
        i++;

        while(av[1][i] > 32)
        {
            write(1, &av[1][i], 1);
            i++;
        }
    }
    write (1, "\n", 1);
}