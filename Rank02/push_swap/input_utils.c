#include "push_swap.h"

static int	is_sign(char c)
{
	return (c == '+' || c == '-');
}

int	is_valid_number(char *str)
{
	int	i;
	int	has_digit;

	if (!str || !str[0])
		return (0);
	i = 0;
	has_digit = 0;
	if (is_sign(str[i]))
		i++;
	while (str[i])
	{
		if (!ft_isdigit(str[i]))
			return (0);
		has_digit = 1;
		i++;
	}
	return (has_digit);
}
