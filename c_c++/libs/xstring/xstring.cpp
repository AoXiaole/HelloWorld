#include<xstring.h>
using namespace std;

/*string 分隔函数 
 *@str 需要被分隔的字符串
 *@pattern 分隔符集合，可以是多个字符
 *return 分隔后的vector向量表*/
vector<string> split( string str, string pattern)
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


