#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>

int is_space(char c)
{
    if (c <= 32)
        return 1;
    return 0;
}

int main(int ac, char **av)
{
    if (ac == 2)
    {
        int i = 0;
        int space = 0;

        while (is_space(av[1][i]))
            i++;

        while (av[1][i])
        {
            if (is_space(av[1][i]))
                space = 1;

            if (!is_space(av[1][i]))
            {
                if (space)
                    write(1, " ", 1);
                space = 0;
                write(1, &av[1][i], 1);
            }
            i++;
        }
    }
    write(1, "\n", 1);
}