/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   routine.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mnassiri <mnassiri@student.1337.ma>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/08/23 18:56:54 by simo              #+#    #+#             */
/*   Updated: 2026/08/28 22:50:24 by mnassiri         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

static void	sim_log(t_sim *sim, t_coder *coder, const char *msg)
{
	pthread_mutex_lock(&sim->log_mtx);
	printf("%lld %d %s\n", get_time_ms() - sim->start_time, coder->id + 1, msg);
	pthread_mutex_unlock(&sim->log_mtx);
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

static void	precise_sleep(long long start_ms)
{
	long long	remaining_time;

	remaining_time = MONITOR_FRAME_BUDGET - (get_time_ms() - start_ms);
	if (remaining_time > 0)
	{
		usleep(remaining_time * 1000);
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
		sim_log(crargs->sim, crargs->coder, "has taken a dongle");
		if (!acquire_dongle(right_d, crargs->coder->id, deadline, crargs->sim))
		{
			release_dongle(left_d, crargs->sim->cooldown);
			break ;
		}
		sim_log(crargs->sim, crargs->coder, "has taken a dongle");
		set_coder_ltc(crargs->coder, get_time_ms());
		sim_log(crargs->sim, crargs->coder, "is compiling");
		usleep(crargs->sim->time_to_compile * 1000);
		release_dongle(right_d, crargs->sim->cooldown);
		release_dongle(left_d, crargs->sim->cooldown);
		inc_coder_compiles(crargs->coder);
		if (sim_should_stop(crargs->sim))
			break ;
		sim_log(crargs->sim, crargs->coder, "is debugging");
		usleep(crargs->sim->time_to_debug * 1000);
		if (sim_should_stop(crargs->sim))
			break ;
		sim_log(crargs->sim, crargs->coder, "is refactoring");
		usleep(crargs->sim->time_to_refactor * 1000);
	}
	return (NULL);
}

void	*monitor_routine(void *arg)
{
	long long	i;
	int			all_coders_done;
	long long	deadline;
	long long	start_ms;
	t_sim		*sim;

	sim = (t_sim *)arg;
	while (1)
	{
		start_ms = get_time_ms();
		i = 0;
		all_coders_done = 1;
		while (i < sim->num_coders)
		{
			deadline = get_coder_ltc(sim->coders[i]) + sim->time_to_burnout;
			if (get_time_ms() >= deadline)
			{
				sim_request_stop(sim);
				sim_log(sim, sim->coders[i], "burned out");
				wake_all_dongles(sim->dongles, sim->num_coders);
				return (NULL);
			}
			if (get_coder_compiles(sim->coders[i]) < sim->required_compiles)
				all_coders_done &= 0;
			i++;
		}
		if (all_coders_done)
		{
			sim_request_stop(sim);
			wake_all_dongles(sim->dongles, sim->num_coders);
			return (NULL);
		}
		precise_sleep(start_ms);
	}
	return (NULL);
}
