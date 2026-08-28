/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mnassiri <mnassiri@student.1337.ma>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/08/22 14:18:07 by mnassiri          #+#    #+#             */
/*   Updated: 2026/08/28 22:30:09 by mnassiri         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

static int	initial_setup(pthread_t *threads, t_sim *sim,
		t_coder_routine_args *crargs)
{
	if (!init_sim(&sim))
	{
		fprintf(stderr, "[ERROR] Failed to intiialize simulation.\n");
		return (0);
	}
	threads = (pthread_t *)malloc(sizeof(pthread_t) * sim->num_coders);
	if (!threads)
	{
		free_sim(&sim);
		return (0);
	}
	crargs = (t_coder_routine_args *)malloc(sizeof(t_coder_routine_args)
			* sim->num_coders);
	if (!crargs)
	{
		free(threads);
		free_sim(&sim);
		return (0);
	}
	return (1);
}

int	main(int ac, char **av)
{
	long long				i;
	t_sim					sim;
	pthread_t				*threads;
	pthread_t				monitor_thread;
	t_coder_routine_args	*crargs;

	if (!parse_args(ac, av, &sim))
		return (-1);
	if (!init_sim(&sim))
	{
		fprintf(stderr, "[ERROR] Failed to intiialize simulation.\n");
		return (-1);
	}
	threads = (pthread_t *)malloc(sizeof(pthread_t) * sim.num_coders);
	if (!threads)
	{
		free_sim(&sim);
		return (-1);
	}
	crargs = (t_coder_routine_args *)malloc(sizeof(t_coder_routine_args)
			* sim.num_coders);
	if (!crargs)
	{
		free(threads);
		free_sim(&sim);
		return (-1);
	}
	i = 0;
	while (i < sim.num_coders)
	{
		crargs[i] = (t_coder_routine_args){.coder = sim.coders[i], .sim = &sim};
		pthread_create(&threads[i], NULL, coder_routine, &crargs[i]);
		i++;
	}
	pthread_create(&monitor_thread, NULL, monitor_routine, &sim);
	i = 0;
	while (i < sim.num_coders)
		pthread_join(threads[i++], NULL);
	pthread_join(monitor_thread, NULL);
	free(threads);
	free(crargs);
	free_sim(&sim);
	return (0);
}
