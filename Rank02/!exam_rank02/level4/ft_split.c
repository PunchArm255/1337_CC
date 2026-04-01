#include <stdlib.h>
#include <stdio.h>

int count_words(char *str)
{
    int i = 0;
    int words = 0;

    while (str[i])
    {
        while (str[i] == ' ' || str[i] == '\t' || str[i] == '\n')
            i++;

        if (str[i])
            words++;

        while (str[i] && !(str[i] == ' ' || str[i] == '\t' || str[i] == '\n'))
            i++;
    }
    return words;
}

char    **ft_split(char *str)
{
    int i = 0;
    int j = 0;
    int k;
    char **res;

    res = (char **)malloc(sizeof(char *) * (count_words(str) + 1));
    if (!res)
        return NULL;

    while (str[i])
    {
        while (str[i] == ' ' || str[i] == '\t' || str[i] == '\n')
            i++;

        if (!str[i])
            break;
        
        k = i;
        while (str[i] && !(str[i] == ' ' || str[i] == '\t' || str[i] == '\n'))
            i++;

        res[j] = (char *)malloc(sizeof(char) * (i - k + 1));
        if (!res[j])
        {
            while (j > 0)
            {
                j--;
                free(res[j])
            }
            free(res);
            return NULL;
        }
        int word_index = 0;

        while (k < i)
        {
            res[j][word_index] = str[k];
            k++;
            word_index++;
        }
        res[j][word_index] = '\0';
        j++;
    }
    res[j] = NULL;
    return res;
}

int main(int ac, char **av)
{
    char **tab = ft_split(av[1]);
    int i = 0;

    if (!tab)
        return (1);
    while (tab[i])
    {
        printf("Word [%d]: %s\n", i, tab[i]);
        i++;
    }
    return (0);
}