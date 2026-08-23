/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   coder.c                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: simo <simo@student.42.fr>                  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/08/22 15:41:51 by mnassiri          #+#    #+#             */
/*   Updated: 2026/08/23 19:31:32 by simo             ###   ########.fr       */
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
	return (coder);
}

void	free_coder(t_coder *coder)
{
	free(coder);
}
