/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   routine.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mnassiri <mnassiri@student.1337.ma>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/08/23 18:56:54 by simo              #+#    #+#             */
/*   Updated: 2026/08/30 14:41:06 by mnassiri         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

void	sim_log(t_sim *sim, t_coder *coder, const char *msg)
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

static int	do_compile_cycle(t_coder_routine_args *cr, t_dongle *left_d,
		t_dongle *right_d)
{
	long long	deadline;

	deadline = get_coder_ltc(cr->coder) + cr->sim->time_to_burnout;
	if (!acquire_dongle(left_d, cr->coder->id, deadline, cr->sim))
		return (0);
	sim_log(cr->sim, cr->coder, "has taken a dongle");
	if (!acquire_dongle(right_d, cr->coder->id, deadline, cr->sim))
	{
		release_dongle(left_d, cr->sim->cooldown);
		return (0);
	}
	sim_log(cr->sim, cr->coder, "has taken a dongle");
	set_coder_ltc(cr->coder, get_time_ms());
	sim_log(cr->sim, cr->coder, "is compiling");
	usleep(cr->sim->time_to_compile * 1000);
	release_dongle(right_d, cr->sim->cooldown);
	release_dongle(left_d, cr->sim->cooldown);
	inc_coder_compiles(cr->coder);
	return (1);
}

void	*coder_routine(void *arg)
{
	t_coder_routine_args	*crargs;
	t_dongle				*left_d;
	t_dongle				*right_d;

	crargs = (t_coder_routine_args *)arg;
	set_coder_ltc(crargs->coder, get_time_ms());
	dongle_reorder(crargs->coder, &left_d, &right_d);
	while (!sim_should_stop(crargs->sim))
	{
		if (!do_compile_cycle(crargs, left_d, right_d))
			break ;
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
