typedef struct      s_list
{
    struct s_list   *next;
    void            *data;
}                   t_list;


t_list	*sort_list(t_list* lst, int (*cmp)(int, int))
{
    int tmp;
    t_list *start;

    start = lst;

    while (lst != NULL && lst->next != NULL)
    {
        if ((*cmp)(lst->data, lst->next->data) == 0)
        {
            tmp = lst->data;
            lst->data = lst->next->data;
            lst->next->data = tmp;

            lst = start;
        }
        else
            lst = lst->next;
    }
    return start;
}