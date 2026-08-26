/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   queue.c                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mnassiri <mnassiri@student.1337.ma>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/08/22 16:10:42 by mnassiri          #+#    #+#             */
/*   Updated: 2026/08/26 14:39:35 by mnassiri         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

static t_ticket	*find_slot(t_queue *q, int coder_id)
{
	if (q->a.coder_id == coder_id)
		return (&q->a);
	if (q->b.coder_id == coder_id)
		return (&q->b);
	return (NULL);
}

t_queue	*init_queue(t_scheduler mode)
{
	t_queue	*q;

	q = (t_queue *)malloc(sizeof(t_queue));
	if (!q)
		return (NULL);
	q->a.coder_id = -1;
	q->b.coder_id = -1;
	q->mode = mode;
	return (q);
}

void	enter_queue(t_queue *q, int coder_id, long long arrival_time,
		long long deadline)
{
	t_ticket	*t;

	t = find_slot(q, -1);
	if (!t)
	{
		fprintf(stderr, "[LOGIC ERROR] Couldn't find empty slot.\n");
		return ;
	}
	t->coder_id = coder_id;
	t->arrival_time = arrival_time;
	t->deadline = deadline;
}

void	leave_queue(t_queue *q, int leaving_coder_id)
{
	t_ticket	*t;

	t = find_slot(q, leaving_coder_id);
	if (t)
		t->coder_id = -1;
}

/*Return coder_id OR -1 (if slot is empty)*/
int	queue_next(t_queue *q)
{
	if (q->a.coder_id == -1 && q->b.coder_id == -1)
		return (-1);
	if (q->a.coder_id == -1)
		return (q->b.coder_id);
	if (q->b.coder_id == -1)
		return (q->a.coder_id);
	if (q->mode == FIFO)
	{
		if (q->a.arrival_time <= q->b.arrival_time)
			return (q->a.coder_id);
		return (q->b.coder_id);
	}
	if (q->a.deadline != q->b.deadline)
	{
		if (q->a.deadline < q->b.deadline)
			return (q->a.coder_id);
		return (q->b.coder_id);
	}
	if (q->a.arrival_time <= q->b.arrival_time)
		return (q->a.coder_id);
	return (q->b.coder_id);
}
