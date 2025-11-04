#include "libft.h"

void	ft_bzero(void	*s, size_t n)
{
	unsigned char	*buff;
	size_t			i;

	i = 0;
	buff = (unsigned char *)s;
	while (i < n)
	{
		buff[i] = 0;
		i++;
	}
}