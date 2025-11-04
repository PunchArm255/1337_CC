#include "libft.h"

void	*ft_memmove(void *dst, const void *src, size_t n)
{
	unsigned char	*d;
	unsigned char	*s;
	size_t			i;

    i = 0;
	d = (unsigned char *)dst;
	s = (unsigned char *)src;
	if (d > s)
		while (n-- > 0) // come back to this!!!
			d[n] = s[n];
	else
    {
		while (i < n)
		{
			d[i] = s[i];
			i++;
		}
    }
	return (dst);
}
