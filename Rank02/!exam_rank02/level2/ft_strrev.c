#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>


char    *ft_strrev(char *str)
{
    int i = 0;
    int j;
    char tmp;

    while (str[j])
        j++;
    
    while(i < j - 1)
    {
        tmp = str[i];
        str[i] = str[j - 1];
        str[j - 1] = tmp;
        i++;
        j--;
    }

    return str;
}

int main()
{
    char *str = "hello";
    printf("%s", ft_strrev(str));
}