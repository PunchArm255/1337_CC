/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_printf.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mnassiri <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/09 21:04:07 by mnassiri          #+#    #+#             */
/*   Updated: 2025/12/14 17:00:08 by mnassiri         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>

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

int	ft_putnbr(int n)
{
	int	len;

	len = 0;
	if (n == -2147483648)
	{
		return (ft_putstr("-2147483648"));
	}
	if (n < 0)
	{
		len += ft_putchar('-');
		n = -n;
	}
	if (n > 9)
	{
		len += ft_putnbr(n / 10);
        	len += ft_putnbr(n % 10);
	}
	else
		len += ft_putchar(n + '0');
	return (len);
}

int	typecheck(char type, va_list args)
{
	if (type == 'c')
		return (ft_putchar(va_arg(args, int)));
	else if (type == 's')
		return (ft_putstr(va_arg(args, char *)));
	else if (type == 'd' || type == 'i')
		return (ft_putnbr(va_arg(args, int)));
	else if (type == 'u')
		return (ft_putnbr(va_arg(args, unsigned int)));
	// else if	(type == 'p')
	//	return (ft_putptr(va_args(args, void *)));
	// else if (type == 'x' || type == 'X')
	//	return (ft_puthex());
	else if (type == '%')
		return (ft_putchar('%'));
	return (-1);
}

int	ft_printf(const char *format, ...)
{
	va_list	args;
	int len;
	int i;

	va_start(args, format);
	i = 0;
	len = 0;
	if (!format)
		return (-1);
	while (format[i])
	{
		if (format[i] == '%')
		{
			if (format[i + 1] == '\0')
				return (-1);
			len += typecheck(format[i + 1], args);
			i++;
		}
		else
			len += ft_putchar(format[i]);
		i++;
	}
	va_end(args);
	return (0);
}

int main(void)
{
	ft_printf("testing printf: %c %s %i %d", 'A', "manal", 22, 55);
}
