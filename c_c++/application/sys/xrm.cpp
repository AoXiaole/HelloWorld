#include<iostream>
#include<fstream>
#include<string>
#include<string.h>

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


string getInput(int argc ,char *argv[])
{
	string buff; 
	string str; 
    ifstream infile;  
	if (argc == 2)
    {	
		infile.open(argv[1]);  
  
		if(!infile)  
			return str;
		getline(infile,str,'\0');
	  	infile.close();  
	}
	else
	{
		getline(cin,str,'\0');
		
	}
	return str;
}

int main(int argc ,char *argv[])
{
	int ret = -1;
	
	string str;  
	str=getInput(argc,argv);
	if(str.size() == 0)
	{
		return 1;
	}	
	vector<string> fileNameVec = split(str," \t\r\n");
	
	if(fileNameVec.empty())
	{
		return 0;
	}

	vector<string>::iterator fileNameVec_iter=fileNameVec.begin();
	for(;fileNameVec_iter != fileNameVec.end();fileNameVec_iter++)
	{
		ret = remove(fileNameVec_iter->c_str());
		if(ret != 0)
		{
			perror("rm:");
		}	
	}

	return 0;

}
