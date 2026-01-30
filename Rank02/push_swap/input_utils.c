/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   input_utils.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mnassiri <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/29 23:14:08 by mnassiri          #+#    #+#             */
/*   Updated: 2026/01/29 23:14:10 by mnassiri         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

static int	is_sign(char c)
{
	return (c == '+' || c == '-');
}

int	is_valid_number(char *str)
{
	int	i;
	int	has_digit;

	if (!str || !str[0])
		return (0);
	i = 0;
	has_digit = 0;
	if (is_sign(str[i]))
		i++;
	while (str[i])
	{
		if (!ft_isdigit(str[i]))
			return (0);
		has_digit = 1;
		i++;
	}
	return (has_digit);
}

void	exit_error(char **args, int argc)
{
	if (argc == 2)
		free_split(args);
	ft_error();
}

void	fill_stack(t_stack **a, char **args, int i, int argc)
{
	t_stack	*new;
	long	nbr;

	while (args[i])
	{
		if (!is_valid_number(args[i]))
			exit_error(args, argc);
		nbr = ft_atoi(args[i]);
		if (nbr > INT_MAX || nbr < INT_MIN)
			exit_error(args, argc);
		new = stack_new((int)nbr);
		stack_add_back(a, new);
		i++;
	}
}
