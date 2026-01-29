/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   radix_sort.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mnassiri <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/29 23:14:39 by mnassiri          #+#    #+#             */
/*   Updated: 2026/01/29 23:14:40 by mnassiri         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

/*
** get_max_bits:
** Returns the number of bits needed to represent the largest index.
** Example: If max index is 3 (binary 11), we need 2 bits.
*/
static int	get_max_bits(t_stack **stack)
{
	t_stack	*head;
	int		max;
	int		max_bits;

	head = *stack;
	max = head->index;
	max_bits = 0;
	while (head)
	{
		if (head->index > max)
			max = head->index;
		head = head->next;
	}
	while ((max >> max_bits) != 0)
		max_bits++;
	return (max_bits);
}

/*
** radix_sort:
** Sorts the stack using bitwise operations.
*/
void	radix_sort(t_stack **stack_a, t_stack **stack_b)
{
	t_stack	*head_a;
	int		i;
	int		j;
	int		size;
	int		max_bits;

	i = 0;
	head_a = *stack_a;
	size = stack_size(head_a);
	max_bits = get_max_bits(stack_a);
	while (i < max_bits)
	{
		j = 0;
		while (j++ < size)
		{
			head_a = *stack_a;
			// Check if the bit at position 'i' is 1.
			// (head_a->index >> i) shifts the index right by i bits.
			// & 1 isolates the last bit.
			if (((head_a->index >> i) & 1) == 1)
				ra(stack_a, 1);
			else
				pb(stack_a, stack_b, 1);
		}
		// Push everything back to A
		while (stack_size(*stack_b) != 0)
			pa(stack_a, stack_b, 1);
		i++;
	}
}
