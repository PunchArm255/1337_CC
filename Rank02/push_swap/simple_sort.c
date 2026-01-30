/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   simple_sort.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mnassiri <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/29 23:14:58 by mnassiri          #+#    #+#             */
/*   Updated: 2026/01/29 23:15:00 by mnassiri         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

/*
** get_min:
** Finds the node with the minimum index.
*/
static int	get_min(t_stack **stack, int val)
{
	t_stack	*head;
	int		min;

	head = *stack;
	min = -1;
	while (head)
	{
		if (head->index != val && (min == -1 || head->index < min))
			min = head->index;
		head = head->next;
	}
	return (min);
}

/*
** sort_3:
** Hardcoded logic to sort 3 numbers in <= 2 moves.
** Assumes stack indices are 0, 1, 2 (or relative rank).
*/
static void	sort_3_part2(t_stack **stack_a, int min, int next_min)
{
	t_stack	*head;

	head = *stack_a;
	if (head->index == next_min)
	{
		if (head->next->index == min)
			sa(stack_a, 1);
		else
			rra(stack_a, 1);
	}
	else
	{
		if (head->next->index == min)
			ra(stack_a, 1);
		else
		{
			sa(stack_a, 1);
			rra(stack_a, 1);
		}
	}
}

void	sort_3(t_stack **stack_a)
{
	t_stack	*head;
	int		min;
	int		next_min;

	head = *stack_a;
	min = get_min(stack_a, -1);
	next_min = get_min(stack_a, min);
	if (head->index == min && head->next->index == next_min)
		return ;
	if (head->index == min)
	{
		ra(stack_a, 1);
		sa(stack_a, 1);
		rra(stack_a, 1);
		return ;
	}
	sort_3_part2(stack_a, min, next_min);
}

/*
** sort_4_5:
** Moves the smallest numbers to B, calls sort_3, then pushes them back.
*/
void	sort_5(t_stack **stack_a, t_stack **stack_b)
{
	int	size;

	size = stack_size(*stack_a);
	while (size--)
	{
		if ((*stack_a)->index == 0 || (*stack_a)->index == 1)
			pb(stack_a, stack_b, 1);
		else
			ra(stack_a, 1);
	}
	sort_3(stack_a);
	pa(stack_a, stack_b, 1);
	pa(stack_a, stack_b, 1);
	if ((*stack_a)->index > (*stack_a)->next->index)
		sa(stack_a, 1);
}

/*
** simple_sort:
** Router for small lists.
*/
void	simple_sort(t_stack **stack_a, t_stack **stack_b)
{
	int	size;

	size = stack_size(*stack_a);
	if (size == 2)
		sa(stack_a, 1);
	else if (size == 3)
		sort_3(stack_a);
	else
		sort_5(stack_a, stack_b);
}
