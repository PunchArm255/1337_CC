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
	char	**args;
	int		i;

	i = 0;
	args = NULL;
	if (argc == 2)
	{
		if (!argv[1] || argv[1][0] == '\0')
			ft_error();
		else
			args = ft_split(argv[1], ' ');

	}
	
	else
	{
		i = 1;
		args = argv;
	}
	leak_check(argc, args);
	fill_stack(a, args, i, argc);
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

	stack_a = NULL;
	stack_b = NULL;
	if (argc < 2)
		return (0);
	init_stack(&stack_a, argc, argv);
	perror("");
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
