# our variables and shit

NAME = libft.a

CC = cc

CFLAGS = -Wall -Wextra -Werror

RM = rm -f

AR = ar rcs

SRCS = ft_isalnum.c \
ft_isalpha.c \
ft_isascii.c \
ft_isdigit.c \
ft_strlen.c \
ft_isprint.c \
ft_memset.c \
ft_bzero.c

OBJ = $(SRCS:.c=.o)

INC = libft.h

# rules and shit apparently

all: $(NAME)

$(NAME) : $(OBJ)
	@echo "CREATING LIBRARY..."
	$(AR) $(NAME) $(OBJ)
	@echo "DONE!"

%.o: %.c
	@$(CC) $(CFLAGS) -c $< -o $@

clean:
	$(RM) $(OBJ)

fclean: clean
	$(RM) $(NAME)

re: fclean all

.PHONY: all clean fclean re