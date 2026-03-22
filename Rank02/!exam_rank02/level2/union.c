#include <unistd.h>
#include <stdlib.h>

int main(int ac, char **av)
{
    int i = 0;
    int seen[256] = {};

    if (ac == 3)
    {
        while (av[1][i])
        {
            seen[(int)av[1][i]] = 1;
            i++;
        }
        i = 0;
        while (av[2][i])
        {
            seen[(int)av[2][i]] = 1;
            i++;
        }
        i = 0;
        while (av[1][i])
        {
            if (seen[(int)av[1][i]])
            {
                write (1, &av[1][i], 1);
                seen[(int)av[1][i]] = 0;
            }
            i++;
        }
        i = 0;
        while (av[2][i])
        {
            if (seen[(int)av[2][i]])
            {
                write (1, &av[2][i], 1);
                seen[(int)av[2][i]] = 0;
            }
            i++;
        }
    }
    write (1, "\n", 1);
}