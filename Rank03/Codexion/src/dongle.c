/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   dongle.c                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mnassiri <mnassiri@student.1337.ma>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/08/22 15:41:44 by mnassiri          #+#    #+#             */
/*   Updated: 2026/08/28 20:21:44 by mnassiri         ###   ########.fr       */
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
	if (!pthread_mutex_init(&dongle->acquire_mtx, NULL))
	{
		free_queue(dongle->queue);
		free(dongle);
		return (NULL);
	}
	if (!pthread_cond_init(&dongle->cond, NULL))
	{
		free_queue(dongle->queue);
		pthread_cond_destroy(&dongle->cond);
		free(dongle);
		return (NULL);
	}
	return (dongle);
}

void	free_dongle(t_dongle *dongle)
{
	if (!dongle)
		return ;
	free_queue(dongle->queue);
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
