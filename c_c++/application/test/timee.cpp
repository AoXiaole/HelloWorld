#include<stdio.h>
#include <time.h>
int main()
{
	unsigned int a=0xffffffff;
	long long  b=0x7fffffffffffffff;
	long long  c=0;
	
	struct timespec ts;
	clock_gettime(CLOCK_REALTIME, &ts);
	c=ts.tv_sec * 1000000 + (ts.tv_nsec / 1000);

	printf("c = %llu\n",c);
	printf("us=%d%d\n",ts.tv_sec,ts.tv_nsec / 1000);
	printf("b =%llu\n",b);	
	
	printf("int s:%d,%u\n",sizeof(int),a);
	printf("64:sizeof(long long)=%d, %llu\n",sizeof(b),b);
}
