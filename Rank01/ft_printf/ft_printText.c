/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_printText.c                                     :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mnassiri <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/14 19:03:47 by mnassiri          #+#    #+#             */
/*   Updated: 2025/12/15 17:28:39 by mnassiri         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"

int	ft_putchar(char c)
{
	write(1, &c, 1);
	return (1);
}

int	ft_putstr(char *s)
{
	int	i;
	int	len;

	i = 0;
	len = 0;
	while (s[i])
	{
		write(1, &s[i], 1);
		i++;
		len++;
	}
	return (len);
}

int	ft_puthex(unsigned long n, char *base)
{
	int	len;

	len = 0;
	if (n >= 16)
	{
		len += ft_puthex(n / 16, base);
		len += ft_puthex(n % 16, base);
	}
	else
		len += ft_putchar(base[n]);
	return (len);
}

int	ft_putptr(void *ptr)
{
	int	len;

	if (ptr == NULL)
		return (ft_putstr("(nil)"));
	len = 0;
	len += ft_putstr("0x");
	len += ft_puthex((unsigned long)ptr, "0123456789abcdef");
	return (len);
}
