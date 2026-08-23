NAME        = codexion
CC          = cc
CFLAGS      = -Wall -Wextra -Werror -pthread
INC         = -I include

SRC_DIR     = src
OBJ_DIR     = obj

SRC_FILES   = main.c parse.c utils.c utils2.c coder.c dongle.c init.c routine.c queue.c
OBJ_FILES   = $(SRC_FILES:.c=.o)

SRC         = $(addprefix $(SRC_DIR)/, $(SRC_FILES))
OBJ         = $(addprefix $(OBJ_DIR)/, $(OBJ_FILES))


all: $(NAME)

$(NAME): $(OBJ)
	$(CC) $(CFLAGS) $(OBJ) -o $(NAME)

$(OBJ_DIR)/%.o: $(SRC_DIR)/%.c | $(OBJ_DIR)
	$(CC) $(CFLAGS) $(INC) -c $< -o $@

$(OBJ_DIR):
	mkdir -p $(OBJ_DIR)

clean:
	rm -rf $(OBJ_DIR)

fclean: clean
	rm -f $(NAME)

re: fclean all

.PHONY: all clean fclean re
