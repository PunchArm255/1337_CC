/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strmapi.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mnassiri <mnassiri@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/06 20:40:20 by mnassiri          #+#    #+#             */
/*   Updated: 2025/11/09 01:23:36 by mnassiri         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

char	*ft_strmapi(const char *s, char (*f)(unsigned int, char))
{
	char			*ss;
	unsigned int	i;

	i = 0;
	if (!s || !f)
		return (NULL);
	ss = malloc(sizeof(char) * (ft_strlen(s) + 1));
	if (!ss)
		return (NULL);
	while (s[i])
	{
		ss[i] = (*f)(i, s[i]);
		i++;
	}
	ss[i] = '\0';
	return (ss);
}
