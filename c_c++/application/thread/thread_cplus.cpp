#include<iostream>
#include<thread>
using namespace std;
void foo()
{
	cout<<"foo function"<<endl;
}

void bar(int x)
{
	cout<<"bar function x= "<<x<<endl;
}

int main()
{
	thread first(foo);
	thread second(bar,2);
	cout<<"main ,foo,bar now execute ...\n";
	first.join();
	second.join();
	cout<<"foo and bar completed\n";

	return 0;	
}
