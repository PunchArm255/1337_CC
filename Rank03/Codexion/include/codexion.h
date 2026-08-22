/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   codexion.h                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mnassiri <mnassiri@student.1337.ma>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/08/22 10:51:24 by mnassiri          #+#    #+#             */
/*   Updated: 2026/08/22 18:41:11 by mnassiri         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef CODEXION_H
# define CODEXION_H

# include <pthread.h>
# include <stdio.h>
# include <stdlib.h>
# include <string.h>
# include <sys/time.h>
# include <unistd.h>

/*=== ENUMS & MACROS ===*/

typedef enum e_scheduler
{
	FIFO,
	EDF
}						t_scheduler;

/*=== STRUCTS ===*/

typedef struct s_sim	t_sim;

typedef struct s_ticket
{
	int					coder_id;
	long long			arrival_time;
	long long			deadline;
}						t_ticket;

typedef struct s_queue
{
	t_ticket			a;
	t_ticket			b;
	t_scheduler			mode;
}						t_queue;

typedef struct s_dongle
{
	int					is_acquired;
	long long			time_to_acquire;

	pthread_mutex_t		acquire_mtx;
	pthread_cond_t		cond;

	t_queue				*queue;

}						t_dongle;

typedef struct s_coder
{
	int					id;
	int					times_compiled;
	long				last_compile_start;

	t_dongle			*left_dongle;
	t_dongle			*right_dongle;
}						t_coder;

struct					s_sim
{
	int					num_coders;
	long				start_time;
	long				time_to_burnout;
	long				time_to_compile;
	long				time_to_debug;
	long				time_to_refactor;
	int					required_compiles;
	long				cooldown;
	t_scheduler			scheduler;

	int					should_stop;

	t_coder				*coders;
	pthread_mutex_t		*dongles;

	pthread_mutex_t		log_mtx;
	pthread_mutex_t		state_mtx;
};

/*=== FUNCTION PROTOTYPES ===*/

/*parse.c*/
int						parse_args(int ac, char **av, t_sim *sim);

/*utils.c*/
long					ft_atol(const char *str);
long					get_time_ms(void);
void					free_queue(t_queue *q);
void					print_long(t_sim *sim, int id, char *msg);
void					ms_to_timespec(struct timespec *ts, long long ms);

/*utils2.c*/
int						sim_should_stop(t_sim *sim);
void					sim_request_stop(t_sim *sim);

/*init.c*/
int						init_sim(t_sim *sim, int id, char *msg);
void					free_sim(t_sim *sim);

/*dongle.c*/
t_dongle				*init_dongle(t_scheduler mode);
void					free_dongle(t_dongle *dongle);
int						acquire_dongle(t_dongle *d, int coder_id,
							long long deadline, t_sim *sim);
void					release_dongle(t_dongle *d, long long cooldown);

/*coder.c*/
t_coder					*init_coder(int id, t_dongle *left_dongle,
							t_dongle *right_dongle);
void					free_coder(t_coder *coder);

/*queue.c*/
t_queue					*init_queue(t_scheduler mode);
void					enter_queue(t_queue *q, int coder_id,
							long long arrival_time, long long deadline);
void					leave_queue(t_queue *q, int leaving_coder_id);
int						queue_next(t_queue *q);

#endif
