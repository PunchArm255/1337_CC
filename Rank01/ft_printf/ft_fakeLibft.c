/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_fakeLibft.c                                     :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mnassiri <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/14 19:03:47 by mnassiri          #+#    #+#             */
/*   Updated: 2025/12/14 19:03:54 by mnassiri         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

int     ft_putchar(char c)
{
        write(1, &c, 1);
        return (1);
}

int     ft_putstr(char *s)
{
        int     i;
        int     len;

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

int     ft_putnbr(int n)
{
        int     len;

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
