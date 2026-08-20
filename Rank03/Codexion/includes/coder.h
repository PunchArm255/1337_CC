/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   coder.h                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mnassiri <mnassiri@student.1337.ma>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/08/20 14:43:55 by mnassiri          #+#    #+#             */
/*   Updated: 2026/08/20 14:57:09 by mnassiri         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef CODER_H
# define CODER_H

typedef struct s_coder
{
	int				id;
	int				times_compiled;
	int				last_compiled_start;
}					t_coder;

t_coder	coder_init(int id, void *left_dongle, void *right_dongle);

void	coder_free(t_coder	*coder);

#endif
