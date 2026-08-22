/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   dongle.c                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mnassiri <mnassiri@student.1337.ma>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/08/22 15:41:44 by mnassiri          #+#    #+#             */
/*   Updated: 2026/08/22 17:17:04 by mnassiri         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

t_dongle	*init_dongle(t_scheduler mode)
{
	t_dongle	*dongle;

	dongle = (t_dongle *)malloc(sizeof(t_dongle));
	if (!dongle)
		return (NULL);
	dongle->queue = init_queue(mode);
	if (!dongle->queue)
	{
		free(dongle);
		return (NULL);
	}
	dongle->is_acquired = 0;
	dongle->time_to_acquire = 0;
	pthread_mutex_init(&dongle->acquire_mtx, NULL);
	pthread_cond_init(&dongle->cond, NULL);
	return (dongle);
}

void	free_dongle(t_dongle *dongle)
{
	pthread_mutex_destroy(&dongle->acquire_mtx);
	pthread_cond_destroy(&dongle->cond);
	free(dongle);
}

static int	must_wait(t_dongle *d, int coder_id)
{
	if (d->is_acquired)
		return (1);
	if (get_time_ms() < d->time_to_acquire)
		return (1);
	if (queue_next(d->queue) != coder_id)
		return (1);
	return (0);
}

int	acquire_dongle(t_dongle *d, int coder_id, long long deadline, t_sim *sim)
{
	pthread_mutex_lock(&d->acquire_mtx);
	enter_queue(d->queue, coder_id, get_time_ms(), deadline);
	while (!sim_should_stop(sim) && must_wait(d, coder_id))
	{
		
	}
	leave_queue(d->queue, coder_id);
	pthread_mutex_unlock(&d->acquire_mtx);
	return (0);
}
