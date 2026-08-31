/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   parse.c                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mnassiri <mnassiri@student.1337.ma>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/08/22 13:31:36 by mnassiri          #+#    #+#             */
/*   Updated: 2026/08/31 01:17:08 by mnassiri         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

static int	is_valid_syntax(const char *str)
{
	int	i;
	int	has_digits;

	i = 0;
	has_digits = 0;
	if (!str || !str[0])
		return (0);
	while ((str[i] >= '\t' && str[i] <= '\r') || str[i] == ' ')
		i++;
	if (str[i] == '+')
		i++;
	while (str[i] >= '0' && str[i] <= '9')
	{
		has_digits = 1;
		i++;
	}
	while ((str[i] >= '\t' && str[i] <= '\r') || str[i] == ' ')
		i++;
	if (!has_digits || str[i] != '\0')
		return (0);
	return (1);
}

static int	validate_syntax_all(char **av)
{
	int	i;

	i = 1;
	while (i <= 7)
	{
		if (!is_valid_syntax(av[i]))
			return (0);
		i++;
	}
	return (1);
}

static int	fill_sim_data(char **av, t_sim *sim)
{
	sim->num_coders = ft_atoll(av[1]);
	sim->time_to_burnout = ft_atoll(av[2]);
	sim->time_to_compile = ft_atoll(av[3]);
	sim->time_to_debug = ft_atoll(av[4]);
	sim->time_to_refactor = ft_atoll(av[5]);
	sim->required_compiles = ft_atoll(av[6]);
	sim->cooldown = ft_atoll(av[7]);
	if (sim->num_coders == 0)
	{
		fprintf(stderr, "[ERROR] Number of coders must be at least 1.\n");
		return (0);
	}
	if (sim->num_coders < 0 || sim->time_to_burnout < 0
		|| sim->time_to_compile < 0 || sim->time_to_debug < 0
		|| sim->time_to_refactor < 0 || sim->required_compiles < 0
		|| sim->cooldown < 0)
	{
		fprintf(stderr, "[ERROR] Arguments out of range or invalid.\n");
		return (0);
	}
	return (1);
}

static int	parse_scheduler(char *av, t_sim *sim)
{
	if (strcmp(av, "fifo") == 0)
		sim->scheduler = FIFO;
	else if (strcmp(av, "edf") == 0)
		sim->scheduler = EDF;
	else
	{
		fprintf(stderr, "[ERROR] Scheduler must be 'fifo' or 'edf'.\n");
		return (0);
	}
	return (1);
}

int	parse_args(int ac, char **av, t_sim *sim)
{
	if (ac != 9)
	{
		fprintf(stderr, "[ERROR] Invalid argument count. Expected 8, got %d.\n",
			ac - 1);
		return (0);
	}
	if (!validate_syntax_all(av))
	{
		fprintf(stderr,
			"[ERROR] Arguments 1-7 must be valid positive integers.\n");
		return (0);
	}
	if (!fill_sim_data(av, sim) || !parse_scheduler(av[8], sim))
		return (0);
	return (1);
}
