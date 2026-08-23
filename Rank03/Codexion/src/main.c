/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: simo <simo@student.42.fr>                  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/08/22 14:18:07 by mnassiri          #+#    #+#             */
/*   Updated: 2026/08/23 19:34:57 by simo             ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

int	main(int ac, char **av)
{
	int						i;
	t_sim					sim;
	pthread_t				*threads;
	pthread_t				monitor_thread;
	t_coder_routine_args	*crargs;

	parse_args(ac, av, &sim);
	if (!init_sim(&sim))
	{
		fprintf(stderr, "[ERROR] Failed to intiialize simulation.\n");
		return (-1);
	}
	threads = (pthread_t *)malloc(sizeof(pthread_t) * sim.num_coders);
	if (!threads)
		return (-1);
	crargs = (t_coder_routine_args *)malloc(sizeof(t_coder_routine_args)
			* sim.num_coders);
	if (!crargs)
	{
		free(threads);
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
	free_sim(&sim);
	printf("[SUCCESS] dakchi bonita <3\n");
	return (0);
}
