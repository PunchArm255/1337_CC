#include "push_swap.h"

/*
** rotate:
** The first element becomes the last one.
*/
static void	rotate(t_stack **stack)
{
	t_stack	*tmp;
	t_stack	*tail;

	if (!*stack || !(*stack)->next)
		return ;
	tmp = *stack;
	*stack = (*stack)->next;
	tail = stack_last(*stack);
	tail->next = tmp;
	tmp->next = NULL;
}

void	ra(t_stack **a, int print)
{
	rotate(a);
	if (print)
		write(1, "ra\n", 3);
}

void	rb(t_stack **b, int print)
{
	rotate(b);
	if (print)
		write(1, "rb\n", 3);
}

void	rr(t_stack **a, t_stack **b, int print)
{
	rotate(a);
	rotate(b);
	if (print)
		write(1, "rr\n", 3);
}