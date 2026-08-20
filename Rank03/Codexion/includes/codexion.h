/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   codexion.h                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mnassiri <mnassiri@student.1337.ma>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/08/20 11:00:28 by mnassiri          #+#    #+#             */
/*   Updated: 2026/08/20 14:54:39 by mnassiri         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef CODEXION_H
# define CODEXION_H

# include <pthread.h>
# include <stdio.h>
# include <stdlib.h>
# include <string.h>
# include <sys/time.h>

typedef enum e_scheduler
{
	FIFO,
	EDF
}		t_scheduler;

typedef struct s_coder
{
	int	id;
	int	times_compiled;
	int	last_compiled_start;
}		t_coder;

#endif
