/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   parser.c                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mnassiri <mnassiri@student.1337.ma>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/08/20 13:13:51 by mnassiri          #+#    #+#             */
/*   Updated: 2026/08/20 14:28:43 by mnassiri         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"
#include "parser.h"

static int	is_valid_uint(const char *s)
{
	if (!s || !*s)
		return (0);
	while (*s)
	{
		if (*s < '0' || *s > '9')
			return (0);
		s++;
	}
	return (1);
}

static int	parse_uint_args(char **argv, t_args *out)
{
	if (!is_valid_uint(argv[1]) || !is_valid_uint(argv[2])
		|| !is_valid_uint(argv[3]) || !is_valid_uint(argv[4])
		|| !is_valid_uint(argv[5]) || !is_valid_uint(argv[6])
		|| !is_valid_uint(argv[7]))
	{
		return (0);
	}
	out->number_of_coders = atoi(argv[1]);
	out->time_to_burnout = atoi(argv[2]);
	out->time_to_compile = atoi(argv[3]);
	out->time_to_debug = atoi(argv[4]);
	out->time_to_refactor = atoi(argv[5]);
	out->number_of_compiles_required = atoi(argv[6]);
	out->dongle_cooldown = atoi(argv[7]);
	return (1);
}

int	parse_args(int argc, char **argv, t_args *out)
{
	if (argc != 9)
	{
		printf("[ERROR] WRONG ARGUMENT COUNT\n");
		return (0);
	}
	if (!parse_uint_args(argv, out))
	{
		printf("[ERROR] ARGUMENTS MUST BE POSITIVE INTEGERS\n");
		return (0);
	}
	if (out->number_of_coders < 1)
	{
		printf("[ERROR] NUMBER OF CODERS MUST BE 1 OR MORE\n");
		return (0);
	}
	if (!strcmp(argv[8], "fifo"))
		out->scheduler = SCHEDULER_FIFO;
	else if (!strcmp(argv[8], "edf"))
		out->scheduler = SCHEDULER_EDF;
	else
	{
		printf("[ERROR] SCHEDULER MUST BE 'FIFO' or 'EDF'\n");
		return (0);
	}
	return (1);
}
