#include <stdio.h>
#include <stdarg.h>

double	avg(int count, ...)
{
	va_list	args;
	int i;
	double total;
	double res;

	va_start(args, count);
	i = 0;
	total = 0;
	res = 0;

	while (i < count)
	{
		total += (double)va_arg(args, int);
		i++;	
	}
	res = total/count;
	return (res);
}

int main()
{
	printf("avg: %.2f", avg(3, 1, 2, 3));
}
