#include <stdio.h>
#include <stdarg.h>

int	sum(int count, ...)
{
	va_list		args;
	int		total;
	int		i;

	i = 0;
	total = 0;
	va_start(args, count);
	while (i < count)
	{
		total += va_arg(args, int);
		i++;
	}
	va_end (args);
	return (total);
}

int main()
{
	printf("sum: %d\n", sum(5, 2,3,4,5,32));
	return (0);
}
