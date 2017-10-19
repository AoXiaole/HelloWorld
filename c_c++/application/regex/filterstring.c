 
#include <regex.h> 
#include <string.h>

#include<iostream>
#include<fstream>

#include<string>
using namespace std;

static int filterString(regex_t *reg,const char *str)
{
    regmatch_t pmatch[1];  
    const size_t nmatch =1 ; 
    int status , i=0;
    
    while(1)
    { 
        memset(pmatch,0,sizeof(pmatch));

        status = regexec(reg,str + i,nmatch,pmatch,0);
		if(status == REG_NOMATCH)  
		{	
			break;
		}
		else if (0 == status)  
		{  			
            write(1,str + i + pmatch[0].rm_so,pmatch[0].rm_eo-pmatch[0].rm_so);
			i = i + pmatch[0].rm_eo;            
			cout<<"\n";           
		}  
    }
    return 0;
}

#if 1

int fileregx(char *fileName,char *pattern)
{

    int cflags = REG_EXTENDED;  
    
    regex_t reg;  

    ifstream myFile(fileName,ios_base::binary);
    if(!myFile)
    {
        cerr<<fileName<<" open error"<<endl;
        return 1;
    }
    
    regcomp(&reg,pattern,cflags);

    string str;
    
    while(!myFile.eof())
    {
        getline(myFile,str,'\0');
        if(str.size() == 0)
            continue;
        filterString(&reg,str.c_str());
    }
    regfree(&reg);
    return 0;
}

int cinregx(char *pattern)
{

    int cflags = REG_EXTENDED;  
    
    regex_t reg;  

    regcomp(&reg,pattern,cflags);

    string str;

    getline(cin,str,'\0');
    filterString(&reg,str.c_str());

    regfree(&reg);
    return 0;
}


int main(int argc ,char *argv[])
{
    long fileLen = 0;
    const char *fileData = NULL;
    char *fileName = NULL;
    char * pattern = NULL;
    string str;
    
    if (argc < 2)
    {
        cerr<<"useage : fileterstring <pattern> [file]\n";
        return 1;
    }
    
    pattern = argv[1];
    
    if(argc == 3)
    {
        fileName = argv[2];
        fileregx(fileName,pattern);
        
    }
    else if(argc == 2)
    {
        cinregx(pattern);
    }
    return 0;  
}


#else
int requestFileData(char *fileName,const char **fileData)
{
    long fileLen ; 

    ifstream myFile(fileName,ios_base::binary);
	
	myFile.seekg(0,myFile.end);
	fileLen = myFile.tellg();
	myFile.seekg(0,myFile.beg);
    
	char * fileBuff = new char[fileLen+1];
    if(fileBuff == NULL)
        return -1;
    
	myFile.read(fileBuff,fileLen);

    *fileData = fileBuff;
    
    return fileLen;
 
    
}

void freeFileData(const char **fileData)
{
    delete [] *fileData;
    *fileData = NULL;
}


int regx(const char *data,long dataLen,const char * pattern)
{  
   
    int ret = 1;
    
   
    long dataIndex = 0;;
   
    int stringlen=0;
    
    int cflags = REG_EXTENDED;  
    
    regex_t reg;  

    regcomp(&reg,pattern,cflags);
	
    while(1)
    {
        
        while(dataIndex < dataLen && data[dataIndex] == 0)
        {
            dataIndex++;
        }

        if(dataIndex == dataLen)
                break;
        
        filterString(&reg,data + dataIndex);
        
        dataIndex = dataIndex + strlen(data + dataIndex) + 1;
        if(dataIndex >= dataLen)
                break;
        
    }

    regfree(&reg); 
	
	
    
    return 0; 
    
    
}

int main(int argc, char *argv[])
{
    long fileLen = 0;
    const char *fileData = NULL;
    char *fileName = NULL;
    char * pattern = NULL;
    string str;
	
    if (argc < 2)
    {
        cerr<<"useage : fileterstring <pattern> [file]\n";
        return 1;
    }
    
    pattern = argv[1];
    
    if(argc == 3)
    {
        fileName = argv[2];
        
        fileLen = requestFileData(fileName,&fileData);
        if(fileLen == -1)
        {
            return 1;
        }
    }
    else if(argc == 2)
    {
        getline(cin,str,'\0');
        fileData = str.c_str();
        fileLen = str.size();
    }

    regx(fileData,fileLen,pattern);
    if(argc == 3)
    {    
        freeFileData(&fileData);
    }
    return 0;
}

#endif

