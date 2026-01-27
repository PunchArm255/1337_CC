#include "push_swap.h"

/*
** push:
** Takes the top node from src and puts it at the top of dest.
*/
static void	push(t_stack **dest, t_stack **src)
{
	t_stack	*tmp;

	if (!*src)
		return ;
	tmp = *src;
	*src = (*src)->next;
	tmp->next = *dest;
	*dest = tmp;
}

void	pa(t_stack **a, t_stack **b, int print)
{
	push(a, b);
	if (print)
		write(1, "pa\n", 3);
}

void	pb(t_stack **a, t_stack **b, int print)
{
	push(b, a);
	if (print)
		write(1, "pb\n", 3);
}