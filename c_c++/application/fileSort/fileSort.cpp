#include<iostream>
#include<fstream>
#include<string>
#include<string.h>

#include<list>
#include<set>
#include <vector>
#include <sys/stat.h>

using namespace std;

class CFileTime{
public:
	time_t fileTime;
	string fileName;
	

	CFileTime(string f_name,time_t f_time):fileTime(f_time),fileName(f_name){}
	bool operator<(CFileTime file)const
	{
		return fileTime<=file.fileTime;
	}
};


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
	struct stat statInfo;
	string str;  
	set<CFileTime> cFileTimeSet;
	
	str=getInput(argc,argv);
	if(str.size() == 0)
	{
		return 1;
	}	
	vector<string> fileNameVec = split(str," \t\r\n");
	
	if(fileNameVec.empty())
	{
		return 1;
	}

	vector<string>::iterator fileNameVec_iter=fileNameVec.begin();
	for(;fileNameVec_iter != fileNameVec.end();fileNameVec_iter++)
	{
		memset(&statInfo,0,sizeof(statInfo));
		ret = stat((*fileNameVec_iter).c_str(),&statInfo);
		if(ret == 0)
		{
			if(!cFileTimeSet.insert(CFileTime(*fileNameVec_iter,statInfo.st_mtime)).second)
            {
                cerr<<*fileNameVec_iter<<" insert error"<<endl;
            }         
        }
		else
		{
			cerr<<*fileNameVec_iter<<" not found"<<endl;
		}
	}
    

	set<CFileTime>::iterator cFileTimeSet_iter=cFileTimeSet.begin();
	for(;cFileTimeSet_iter!=cFileTimeSet.end();cFileTimeSet_iter++)
		cout<<(*cFileTimeSet_iter).fileName<<endl;
	return 0;



}
