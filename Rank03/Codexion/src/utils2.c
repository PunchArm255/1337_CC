/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   utils2.c                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mnassiri <mnassiri@student.1337.ma>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/08/22 17:03:58 by mnassiri          #+#    #+#             */
/*   Updated: 2026/08/30 16:40:01 by mnassiri         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

int	sim_should_stop(t_sim *sim)
{
	int	val;

	pthread_mutex_lock(&sim->state_mtx);
	val = sim->should_stop;
	pthread_mutex_unlock(&sim->state_mtx);
	return (val);
}

void	sim_request_stop(t_sim *sim)
{
	pthread_mutex_lock(&sim->state_mtx);
	sim->should_stop = 1;
	pthread_mutex_unlock(&sim->state_mtx);
}

long long	get_coder_ltc(t_coder *c)
{
	long long	val;

	pthread_mutex_lock(&c->mtx);
	val = c->last_compile_start;
	pthread_mutex_unlock(&c->mtx);
	return (val);
}

void	set_coder_ltc(t_coder *c, long long val)
{
	pthread_mutex_lock(&c->mtx);
	c->last_compile_start = val;
	pthread_mutex_unlock(&c->mtx);
}

void	wake_all_dongles(t_dongle **ds, int num_dongles)
{
	int	i;

	i = 0;
	while (i < num_dongles)
	{
		pthread_mutex_lock(&ds[i]->acquire_mtx);
		pthread_cond_broadcast(&ds[i]->cond);
		pthread_mutex_unlock(&ds[i]->acquire_mtx);
		i++;
	}
}
