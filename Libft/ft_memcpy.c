#include "libft.h"

void	*ft_memcpy(void *dst, const void *src, size_t n)
{
    unsigned char   *d;
    unsigned char   *s;
    size_t          i;

    i = 0;
    d = (unsigned char *)dst;
    s = (unsigned char *)src;
    if (!src && !dst)
        return (dst);
    while (i < n)
    {
        d[i] = s[i];
        i++;
    }
    return (dst);
}