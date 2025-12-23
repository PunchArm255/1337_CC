NAME = libftprintf.a

CC = cc

CFLAGS = -Wall -Wextra -Werror

RM = rm -f

AR = ar rcs

SRCS = ft_printf.c \
ft_printText.c \
ft_printNum.c

OBJ = $(SRCS:.c=.o)

all: $(NAME)

$(NAME) : $(OBJ)
	@echo "CREATING LIBRARY..."
	$(AR) $(NAME) $(OBJ)
	@echo "DONE!"

%.o: %.c ft_printf.h
	@$(CC) $(CFLAGS) -c $< -o $@

clean:
	$(RM) $(OBJ)

fclean: clean
	$(RM) $(NAME)

re: fclean all

.PHONY: all clean fclean re
