/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   coder.c                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mnassiri <mnassiri@student.1337.ma>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/08/22 15:41:51 by mnassiri          #+#    #+#             */
/*   Updated: 2026/08/26 14:39:43 by mnassiri         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

t_coder	*init_coder(int id, t_dongle *left_dongle, t_dongle *right_dongle)
{
	t_coder	*coder;

	coder = (t_coder *)malloc(sizeof(t_coder));
	if (!coder)
		return (NULL);
	coder->id = id;
	coder->times_compiled = 0;
	coder->last_compile_start = 0;
	coder->left_dongle = left_dongle;
	coder->right_dongle = right_dongle;
	pthread_mutex_init(&coder->mtx, NULL);
	return (coder);
}

void	free_coder(t_coder *coder)
{
	if (!coder)
		return ;
	pthread_mutex_destroy(&coder->mtx);
	free(coder);
}

int	get_coder_compiles(t_coder *c)
{
	int	val;

	pthread_mutex_lock(&c->mtx);
	val = c->times_compiled;
	pthread_mutex_unlock(&c->mtx);
	return (val);
}

void	inc_coder_compiles(t_coder *c)
{
	pthread_mutex_lock(&c->mtx);
	c->times_compiled++;
	pthread_mutex_unlock(&c->mtx);
}
