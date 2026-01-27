#include "push_swap.h"

/*
** swap:
** Swaps the top two elements of the stack.
** Does nothing if there are less than 2 elements.
*/
static void	swap(t_stack **head)
{
	t_stack	*tmp;

	if (!*head || !(*head)->next)
		return ;
	tmp = *head;
	*head = (*head)->next;
	tmp->next = (*head)->next;
	(*head)->next = tmp;
}

void	sa(t_stack **a, int print)
{
	swap(a);
	if (print)
		write(1, "sa\n", 3);
}

void	sb(t_stack **b, int print)
{
	swap(b);
	if (print)
		write(1, "sb\n", 3);
}

void	ss(t_stack **a, t_stack **b, int print)
{
	swap(a);
	swap(b);
	if (print)
		write(1, "ss\n", 3);
}