#include <unistd.h>

unsigned int    lcm(unsigned int a, unsigned int b)
{
    int n;

    if (a == 0 || b == 0)
        return 0;

    (a > b) ? n = a : n = b;

    while (1)
    {
        if ((n % a == 0) && (n % b == 0))
            return g;
        g++;
    }
}