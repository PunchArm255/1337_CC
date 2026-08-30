/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   dongle2.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mnassiri <mnassiri@student.1337.ma>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/08/28 23:00:00 by mnassiri          #+#    #+#             */
/*   Updated: 2026/08/28 23:00:00 by mnassiri         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

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
	long long		wake;
	struct timespec	ts;

	pthread_mutex_lock(&d->acquire_mtx);
	enter_queue(d->queue, coder_id, get_time_ms(), deadline);
	while (!sim_should_stop(sim) && must_wait(d, coder_id))
	{
		wake = deadline;
		if (d->time_to_acquire != 0 && d->time_to_acquire < deadline)
			wake = d->time_to_acquire;
		ms_to_timespec(&ts, wake);
		pthread_cond_timedwait(&d->cond, &d->acquire_mtx, &ts);
	}
	if (sim_should_stop(sim))
	{
		leave_queue(d->queue, coder_id);
		pthread_mutex_unlock(&d->acquire_mtx);
		return (0);
	}
	d->is_acquired = 1;
	leave_queue(d->queue, coder_id);
	pthread_mutex_unlock(&d->acquire_mtx);
	return (1);
}

void	release_dongle(t_dongle *d, long long cooldown)
{
	pthread_mutex_lock(&d->acquire_mtx);
	d->is_acquired = 0;
	d->time_to_acquire = get_time_ms() + cooldown;
	pthread_cond_broadcast(&d->cond);
	pthread_mutex_unlock(&d->acquire_mtx);
}
