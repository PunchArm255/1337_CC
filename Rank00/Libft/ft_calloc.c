/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_calloc.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mnassiri <mnassiri@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/05 23:59:01 by mnassiri          #+#    #+#             */
/*   Updated: 2025/11/11 21:16:28 by mnassiri         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

void	*ft_calloc(size_t count, size_t size)
{
	unsigned char	*tmp;
	size_t			total_size;

	total_size = count * size;
	if (count == 0 || size == 0)
	{
		tmp = malloc(1);
		return (tmp);
	}
	if (size != 0 && count > SIZE_MAX / size)
		return (NULL);
	tmp = malloc(total_size);
	if (!tmp)
		return (NULL);
	ft_memset(tmp, 0, total_size);
	return (tmp);
}
