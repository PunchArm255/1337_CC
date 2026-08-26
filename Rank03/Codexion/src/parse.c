/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   parse.c                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mnassiri <mnassiri@student.1337.ma>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/08/22 13:31:36 by mnassiri          #+#    #+#             */
/*   Updated: 2026/08/26 22:24:02 by mnassiri         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

static int	is_valid_number(const char *str)
{
	int	i;

	i = 0;
	if (!str || !str[0])
		return (0);
	while (str[i])
	{
		if (str[i] < '0' || str[i] > '9')
			return (0);
		i++;
	}
	return (1);
}

static int	validate_all_numbers(char **av)
{
	int	i;

	i = 1;
	while (i <= 7)
	{
		if (!is_valid_number(av[i]))
			return (0);
		i++;
	}
	return (1);
}

static void	fill_sim_data(char **av, t_sim *sim)
{
	sim->num_coders = ft_atoll(av[1]);
	sim->time_to_burnout = ft_atoll(av[2]);
	sim->time_to_compile = ft_atoll(av[3]);
	sim->time_to_debug = ft_atoll(av[4]);
	sim->time_to_refactor = ft_atoll(av[5]);
	sim->required_compiles = ft_atoll(av[6]);
	sim->cooldown = ft_atoll(av[7]);
	sim->should_stop = 0;
}

static int	parse_scheduler(char *av, t_sim *sim)
{
	if (strcmp(av, "fifo") == 0)
		sim->scheduler = FIFO;
	else if (strcmp(av, "edf") == 0)
		sim->scheduler = EDF;
	else
	{
		printf("[ERROR] Scheduler must be 'fifo' or 'edf'.\n");
		return (0);
	}
	return (1);
}

int	parse_args(int ac, char **av, t_sim *sim)
{
	if (ac != 9)
	{
		printf("[ERROR] Invalid argument count. Expected 8, got %d.\n", ac - 1);
		return (0);
	}
	if (!validate_all_numbers(av))
	{
		printf("[ERROR] Arguments 1-7 must be positive numbers.\n");
		return (0);
	}
	fill_sim_data(av, sim);
	if (sim->num_coders < 1)
	{
		printf("[ERROR] Number of coders must be at least 1.\n");
		return (0);
	}
	if (!parse_scheduler(av[8], sim))
		return (0);
	return (1);
}
