/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   sim.h                                              :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mnassiri <mnassiri@student.1337.ma>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/08/20 14:36:22 by mnassiri          #+#    #+#             */
/*   Updated: 2026/08/20 18:31:55 by mnassiri         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef SIM_H
# define SIM_H

# include <coder.h>
# include <pthread.h>

typedef struct s_sim
{
	unsigned int	number_of_coders;
	unsigned int	time_to_burnout;
	unsigned int	time_to_compile;
	unsigned int	time_to_debug;
	unsigned int	time_to_refactor;
	unsigned int	number_of_compiles_required;
	unsigned int	dongle_cooldown;
	unsigned int	schedule;
	int				should_stop;
	void			**dongles;
	t_coder			**coders;
	pthread_mutex_t	log_mtx;
	pthread_mutex_t	state_mtx;

}					t_sim;

t_sim				*sim_init(t_args *args);

int					sim_should_stop(t_sim *sim);

void				sim_request_stop(t_sim *sim);

void				sim_free(t_sim *sim);

#endif
