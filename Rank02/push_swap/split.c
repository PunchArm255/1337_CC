#include "push_swap.h"

static char	**mem_free(char **poof)
{
	int	i;

	i = 0;
	if (!poof)
		return (NULL);
	while (poof[i])
	{
		free(poof[i]);
		i++;
	}
	free(poof);
	return (NULL);
}

static size_t	count_words(const char *str, char sep)
{
	int	i;
	int	words;

	i = 0;
	words = 0;
	while (str[i])
	{
		while (str[i] && (str[i] == sep))
			i++;
		if (str[i])
			words++;
		while (str[i] && !(str[i] == sep))
			i++;
	}
	return (words);
}

static void	locate_words(char **cursor, size_t *word_len, char sep)
{
	size_t	i;

	*cursor += *word_len;
	*word_len = 0;
	i = 0;
	while (**cursor && **cursor == sep)
		(*cursor)++;
	while ((*cursor)[i])
	{
		if ((*cursor)[i] == sep)
			return ;
		(*word_len)++;
		i++;
	}
}

void	free_split(char **args)
{
	int	i;

	if (!args)
		return ;
	i = 0;
	while (args[i])
	{
		free(args[i]);
		i++;
	}
	free(args);
}

char	**ft_split(const char *str, char sep)
{
	char	**result;
	char	*cursor;
	size_t	word_len;
	size_t	i;

	if (!str)
		return (NULL);
	result = malloc(sizeof(char *) * (count_words(str, sep) + 1));
	if (!result)
		return (NULL);
	i = 0;
	cursor = (char *)str;
	word_len = 0;
	while (i < count_words(str, sep))
	{
		locate_words(&cursor, &word_len, sep);
		result[i] = malloc(sizeof(char) * (word_len + 1));
		if (!result[i])
			return (mem_free(result));
		ft_strlcpy(result[i], cursor, word_len + 1);
		i++;
	}
	result[i] = NULL;
	return (result);
}
