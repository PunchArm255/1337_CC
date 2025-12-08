/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_memset.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mnassiri <mnassiri@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/04 21:04:53 by mnassiri          #+#    #+#             */
/*   Updated: 2025/11/14 23:51:17 by mnassiri         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

void	*ft_memset(void *s, int c, size_t n)
{
	unsigned char	*buff;
	size_t			i;

	i = 0;
	buff = (unsigned char *)s;
	while (i < n)
	{
		buff[i] = c;
		i++;
	}
	return (buff);
}
