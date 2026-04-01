void    ft_swap(int *a, int *b)
{
    int tmp;

    tmp = *a;
    *a = *b;
    *b = tmp;
}

void sort_int_tab(int *tab, unsigned int size)
{
    int i = 0;
    int j = size - 1;

    while (i < j)
    {
        if (tab[i] > tab[i+1])
        {
            ft_swap(&tab[i], &tab[i+1]);
            i = 0;
        }
        else
            i++;
    }
}