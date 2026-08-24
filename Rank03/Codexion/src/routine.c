/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   routine.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: simo <simo@student.42.fr>                  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/08/23 18:56:54 by simo              #+#    #+#             */
/*   Updated: 2026/08/24 23:52:18 by simo             ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

void	*coder_routine(void *arg)
{
	t_coder_routine_args	*crargs;
	long long				deadline;

	crargs = (t_coder_routine_args *)arg;
	crargs->coder->last_compile_start = get_time_ms();
	while (!sim_should_stop(crargs->sim))
	{
		deadline = crargs->coder->last_compile_start
			+ crargs->sim->time_to_burnout;
		if (acquire_dongle(crargs->coder->left_dongle, crargs->coder->id,
				deadline, crargs->sim))
			break ;
	}
	return (arg);
}
void	*monitor_routine(void *arg)
{
	return (arg);
}