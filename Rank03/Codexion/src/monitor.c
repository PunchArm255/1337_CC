/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   monitor.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mnassiri <mnassiri@student.1337.ma>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/08/28 23:00:00 by mnassiri          #+#    #+#             */
/*   Updated: 2026/08/28 23:00:00 by mnassiri         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

static void	precise_sleep(long long start_ms)
{
	long long	remaining_time;

	remaining_time = MONITOR_FRAME_BUDGET - (get_time_ms() - start_ms);
	if (remaining_time > 0)
	{
		usleep(remaining_time * 1000);
	}
}

static int	check_coders(t_sim *sim, int *all_done)
{
	long long	i;
	long long	deadline;

	i = 0;
	*all_done = 1;
	while (i < sim->num_coders)
	{
		deadline = get_coder_ltc(sim->coders[i]) + sim->time_to_burnout;
		if (get_time_ms() >= deadline)
		{
			sim_request_stop(sim);
			sim_log(sim, sim->coders[i], "burned out");
			wake_all_dongles(sim->dongles, sim->num_coders);
			return (0);
		}
		if (get_coder_compiles(sim->coders[i]) < sim->required_compiles)
			*all_done = 0;
		i++;
	}
	return (1);
}

void	*monitor_routine(void *arg)
{
	int			all_coders_done;
	long long	start_ms;
	t_sim		*sim;

	sim = (t_sim *)arg;
	while (1)
	{
		start_ms = get_time_ms();
		if (!check_coders(sim, &all_coders_done))
			return (NULL);
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
