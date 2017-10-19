#include<iostream>
#include<string>
#include<string.h>

#include<list>
#include<set>
#include <vector>
#include <sys/stat.h>

using namespace std;


vector< string> split( string str, string pattern)
{
	vector<string> ret;
	if(pattern.empty()) 
		return ret;
	
	size_t start=0,index=str.find_first_of(pattern,0);
	while(index!=str.npos)
	{
		if(start!=index)
			ret.push_back(str.substr(start,index-start));
		start=index+1;
		index=str.find_first_of(pattern,start);
	}
	if(!str.substr(start).empty())
		ret.push_back(str.substr(start));
	return ret;
}



int main(int argc ,char *argv[])
{

	map<string,vector<string>> map_list;
	map_list["1"]=new vector();
	map_list["1"].second

}
