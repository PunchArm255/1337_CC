/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   routine.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: simo <simo@student.42.fr>                  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/08/23 18:56:54 by simo              #+#    #+#             */
/*   Updated: 2026/08/26 00:11:58 by simo             ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

static void	log(t_coder_routine_args *crargs, const char *msg)
{
	pthread_mutex_lock(&crargs->sim->log_mtx);
	printf("%lld %d %s\n", get_time_ms() - crargs->sim->start_time,
		crargs->coder->id + 1, msg);
	pthread_mutex_unlock(&crargs->sim->log_mtx);
}

static void	dongle_reorder(t_coder *c, t_dongle **left, t_dongle **right)
{
	if ((c->id % 2) == 0)
	{
		*left = c->right_dongle;
		*right = c->left_dongle;
	}
	else
	{
		*left = c->left_dongle;
		*right = c->right_dongle;
	}
}

void	*coder_routine(void *arg)
{
	t_coder_routine_args	*crargs;
	long long				deadline;
	t_dongle				*left_d;
	t_dongle				*right_d;

	crargs = (t_coder_routine_args *)arg;
	set_coder_ltc(crargs->coder, get_time_ms());
	dongle_reorder(crargs->coder, &left_d, &right_d);
	while (!sim_should_stop(crargs->sim))
	{
		deadline = get_coder_ltc(crargs->coder) + crargs->sim->time_to_burnout;
		if (!acquire_dongle(left_d, crargs->coder->id, deadline, crargs->sim))
			break ;
		log(crargs, "has taken a left dongle");
		if (!acquire_dongle(right_d, crargs->coder->id, deadline, crargs->sim))
		{
			release_dongle(left_d, crargs->sim->cooldown);
			break ;
		}
		log(crargs, "has taken a right dongle");
		set_coder_ltc(crargs->coder, get_time_ms());
		log(crargs, "is compiling");
		usleep(crargs->sim->time_to_compile);
		release_dongle(right_d, crargs->sim->cooldown);
		release_dongle(left_d, crargs->sim->cooldown);
		inc_coder_compiles(crargs->coder);
		if (sim_should_stop(crargs->sim))
			break ;
		log(crargs, "is debugging");
		usleep(crargs->sim->time_to_debug);
		if (sim_should_stop(crargs->sim))
			break ;
		log(crargs, "is refactoring");
		usleep(crargs->sim->time_to_refactor);
	}
	return (arg);
}
void	*monitor_routine(void *arg)
{
	return (arg);
}