/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_itoa.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mnassiri <mnassiri@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/08 02:57:14 by mnassiri          #+#    #+#             */
/*   Updated: 2025/11/09 22:31:59 by mnassiri         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

static int	string_size(int n)
{
	size_t			size;
	unsigned int	nb;

	size = 0;
	if (n == 0)
		size = 1;
	if (n < 0)
	{
		nb = -n;
		size = 1;
	}
	else
		nb = n;
	while (nb != 0)
	{
		nb = nb / 10;
		size++;
	}
	return (size);
}

static void	string_fill(char *str, int n, int size)
{
	unsigned int	nb;
	unsigned int	size_2;

	size_2 = size - 1;
	if (n == 0)
		str[0] = '0';
	if (n < 0)
	{
		nb = -n;
		str[0] = '-';
	}
	else
		nb = n;
	while (nb != 0)
	{
		str[size_2] = nb % 10 + '0';
		nb = nb / 10;
		size_2--;
	}
	str[size] = '\0';
}

char	*ft_itoa(int n)
{
	char	*str;
	size_t	size;

	size = string_size(n);
	str = malloc(sizeof(char) * size + 1);
	if (!str)
		return (NULL);
	string_fill(str, n, size);
	return (str);
}
