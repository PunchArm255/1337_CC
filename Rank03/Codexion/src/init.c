/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   init.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mnassiri <mnassiri@student.1337.ma>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/08/22 14:59:13 by mnassiri          #+#    #+#             */
/*   Updated: 2026/08/30 16:47:08 by mnassiri         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

static int	init_sim_dongles(t_sim *sim)
{
	long long	i;
	long long	j;

	i = 0;
	sim->dongles = (t_dongle **)malloc(sizeof(t_dongle *) * sim->num_coders);
	if (!sim->dongles)
		return (0);
	while (i < sim->num_coders)
	{
		sim->dongles[i] = init_dongle(sim->scheduler);
		if (!sim->dongles[i])
		{
			j = 0;
			while (j < i)
				free_dongle(sim->dongles[j++]);
			free(sim->dongles);
			return (0);
		}
		i++;
	}
	return (1);
}

static int	init_sim_coders(t_sim *sim)
{
	long long	i;
	long long	j;

	sim->coders = (t_coder **)malloc(sizeof(t_coder *) * sim->num_coders);
	if (!sim->coders)
		return (0);
	i = sim->num_coders;
	while (i-- > 0)
	{
		sim->coders[i] = init_coder(i, sim->dongles[i], sim->dongles[(i + 1)
				% sim->num_coders]);
		if (!sim->coders[i])
		{
			j = 0;
			while (j < i)
				free_coder(sim->coders[j++]);
			free(sim->coders);
			j = 0;
			while (j < sim->num_coders)
				free_dongle(sim->dongles[j++]);
			free(sim->coders);
			return (0);
		}
	}
	return (1);
}

int	init_sim(t_sim *sim)
{
	long long	i;

	if (sim->required_compiles == 0)
		sim->should_stop = 1;
	else
		sim->should_stop = 0;
	sim->start_time = get_time_ms();
	if (!init_sim_dongles(sim))
		return (0);
	if (!init_sim_coders(sim))
		return (0);
	if (pthread_mutex_init(&sim->log_mtx, NULL) != 0
		|| pthread_mutex_init(&sim->state_mtx, NULL) != 0)
	{
		i = -1;
		while (++i < sim->num_coders)
		{
			free_coder(sim->coders[i]);
			free_dongle(sim->dongles[i]);
		}
		free(sim->coders);
		free(sim->dongles);
		return (0);
	}
	return (1);
}

void	free_sim(t_sim *sim)
{
	long long	i;

	i = 0;
	while (i < sim->num_coders)
	{
		free_coder(sim->coders[i]);
		free_dongle(sim->dongles[i]);
		i++;
	}
	pthread_mutex_destroy(&sim->log_mtx);
	pthread_mutex_destroy(&sim->state_mtx);
	free(sim->coders);
	free(sim->dongles);
}
