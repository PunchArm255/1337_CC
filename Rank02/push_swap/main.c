/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mnassiri <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/29 23:14:16 by mnassiri          #+#    #+#             */
/*   Updated: 2026/01/29 23:14:17 by mnassiri         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

static void	index_stack(t_stack *stack_a)
{
	t_stack	*ptr;
	t_stack	*current;

	ptr = stack_a;
	while (ptr)
	{
		ptr->index = 0;
		current = stack_a;
		while (current)
		{
			if (ptr->value > current->value)
				ptr->index++;
			current = current->next;
		}
		ptr = ptr->next;
	}
}

static void	check_duplicates(t_stack *stack)
{
	t_stack	*tmp;

	while (stack)
	{
		tmp = stack->next;
		while (tmp)
		{
			if (stack->value == tmp->value)
				ft_error();
			tmp = tmp->next;
		}
		stack = stack->next;
	}
}

static void	init_stack(t_stack **a, int argc, char **argv)
{
	t_stack	*new;
	char	**args;
	long	nbr;
	int		i;

	i = 0;
	args = NULL;
	if (argc == 2)
		args = ft_split(argv[1], ' ');
	else
	{
		i = 1;
		args = argv;
	}
	if (!args || !args[0])
	{
		if (argc == 2 && args)
			free_split(args);
		return ;
	}
	while (args[i])
	{
		if (!is_valid_number(args[i]))
		{
			if (argc == 2)
				free_split(args);
			ft_error();
		}
		nbr = ft_atoi(args[i]);
		if (nbr > INT_MAX || nbr < INT_MIN)
		{
			if (argc == 2)
				free_split(args);
			ft_error();
		}
		new = stack_new((int)nbr);
		stack_add_back(a, new);
		i++;
	}
	if (argc == 2)
		free_split(args);
	check_duplicates(*a);
}

int	is_sorted(t_stack *stack)
{
	while (stack->next)
	{
		if (stack->value > stack->next->value)
			return (0);
		stack = stack->next;
	}
	return (1);
}

int	main(int argc, char **argv)
{
	t_stack	*stack_a;
	t_stack	*stack_b;

	if (argc < 2)
		return (0);
	stack_a = NULL;
	stack_b = NULL;
	init_stack(&stack_a, argc, argv);
	if (!stack_a)
		return (0);
	index_stack(stack_a);
	if (is_sorted(stack_a))
	{
		free_stack(&stack_a);
		return (0);
	}
	if (stack_size(stack_a) <= 5)
		simple_sort(&stack_a, &stack_b);
	else
		radix_sort(&stack_a, &stack_b);
	free_stack(&stack_a);
	free_stack(&stack_b);
	return (0);
}
