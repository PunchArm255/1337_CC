/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   dongle.c                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mnassiri <mnassiri@student.1337.ma>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/08/22 15:41:44 by mnassiri          #+#    #+#             */
/*   Updated: 2026/08/28 20:21:44 by mnassiri         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

static int	init_dongle_sync(t_dongle *dongle)
{
	if (pthread_mutex_init(&dongle->acquire_mtx, NULL) != 0)
	{
		free_queue(dongle->queue);
		free(dongle);
		return (0);
	}
	if (pthread_cond_init(&dongle->cond, NULL) != 0)
	{
		free_queue(dongle->queue);
		pthread_mutex_destroy(&dongle->acquire_mtx);
		free(dongle);
		return (0);
	}
	return (1);
}

t_dongle	*init_dongle(t_scheduler mode)
{
	t_dongle	*dongle;

	dongle = (t_dongle *)malloc(sizeof(t_dongle));
	if (!dongle)
		return (NULL);
	dongle->queue = init_queue(mode);
	if (!dongle->queue)
	{
		free(dongle);
		return (NULL);
	}
	dongle->is_acquired = 0;
	dongle->time_to_acquire = 0;
	if (!init_dongle_sync(dongle))
		return (NULL);
	return (dongle);
}

void	free_dongle(t_dongle *dongle)
{
	if (!dongle)
		return ;
	free_queue(dongle->queue);
	pthread_mutex_destroy(&dongle->acquire_mtx);
	pthread_cond_destroy(&dongle->cond);
	free(dongle);
}
