#include <stdlib.h>
#include <stdio.h>

char **ft_split(char *str)
{
    int i = 0;
    int j = 0;
    int k;
    char **out;

    // Step 1: Oversize the main array to avoid a word-count function
    while (str[i])
        i++;
    out = (char **)malloc(sizeof(char *) * (i + 1));
    if (!out)
        return (NULL);

    i = 0;
    // Step 2: The Main Traversal
    while (str[i])
    {
        // Skip all whitespace (spaces, tabs, newlines)
        while (str[i] == ' ' || str[i] == '\t' || str[i] == '\n')
            i++;
            
        // If we hit the end of the string while skipping spaces, stop
        if (!str[i])
            break;
            
        // Step 3: Measure the word length
        k = i;
        while (str[i] && str[i] != ' ' && str[i] != '\t' && str[i] != '\n')
            i++;
            
        // Step 4: Allocate exact memory for the word and copy it over
        out[j] = (char *)malloc(sizeof(char) * (i - k + 1));
        int word_index = 0;
        
        while (k < i)
        {
            out[j][word_index] = str[k];
            word_index++;
            k++;
        }
        out[j][word_index] = '\0'; // Null-terminate the new word
        j++;
    }
    
    // Step 5: Null-terminate the entire array
    out[j] = NULL;
    return (out);
}

int main(void)
{
    char **tab = ft_split(" ");
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