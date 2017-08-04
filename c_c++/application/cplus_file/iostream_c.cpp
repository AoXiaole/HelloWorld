#include<iostream>
#include<fstream>
#include<string>
#include <stdio.h>  
#include <sys/types.h>  
#include <regex.h> 
#include <string.h> 
#include <string>
#include <regex>

using namespace std;

void writeOnly_file1(char * fileName,string str)
{
	ofstream myFile(fileName,ios_base::app | ios_base::binary);
	myFile<<str;
}

void writeOnly_file2(char * fileName)
{
	ofstream myFile;
	myFile.open(fileName,ios_base::app); //打开一个文件，也切换，打开其他文件，但需要关闭之前打开的
	myFile<<fileName<<"hahah"<<endl;
	myFile.close();
} 

class Xifstream:public ifstream
{
private:
	char *fileBuff;
	int fileLen;
public:
	Xifstream(){fileBuff = NULL;fileLen = 0;}
	Xifstream (const char* filename, ios_base::openmode mode = ios_base::in):ifstream(filename,mode)
	{
		this->seekg(0,this->end);
		fileLen = this->tellg();
		this->seekg(0,this->beg);
		fileBuff = new char[fileLen];
		this->read(fileBuff,fileLen);
		this->seekg(0,this->beg);
	}
	void open (const char* filename,  ios_base::openmode mode = ios_base::in)
	{
			ifstream::open(filename,mode);
			
			this->seekg(0,this->end);
			fileLen = this->tellg();
			this->seekg(0,this->beg);
			
			if(fileBuff != NULL)
				delete[] fileBuff;
			
			fileBuff = new char[fileLen];
			this->read(fileBuff,fileLen);
			this->seekg(0,this->beg);
	}
	char *data(){return fileBuff;}
	int len(){return fileLen;}
	
	~Xifstream()
	{
		if(fileBuff != NULL)
			delete[] fileBuff;
	}
};

void tt(char *fileName)
{
	Xifstream myFile(fileName,ios_base::binary);
	
	char *filedata = myFile.data();
	int filelen  = myFile.len();

	ofstream ofile("tt",ios_base::binary);
	ofile.write(filedata,filelen);
}
void regx(char *fileName,const char * pattern)
{  
    int status ,i;  
    int cflags = REG_EXTENDED;  
    regmatch_t pmatch[1];  
    const size_t nmatch =1 ;  
    regex_t reg;  
//    const char * pattern = "^\\w+([-+.]\\w+)*@\\w+([-.]\\w+)*.\\w+([-.]\\w+)*$";
	
    char * buf = "chenj456iayi@126.com"; 


	Xifstream myFile(fileName,ios_base::binary);
	
	char *filedata = myFile.data();
	int filelen  = myFile.len();
	i=0;
	while(i<filelen)
	{
			if(filedata[i] == 0)
				filedata[i] = 1;
			i++;
	}

	
    regcomp(&reg,pattern,cflags);//编译正则模式  
	int match_p=0;
    while(1)
	{
		memset(pmatch,0,sizeof(pmatch));
		status = regexec(&reg,filedata + match_p,nmatch,pmatch,0);//执行正则表达式和缓存的比较  
		if(status == REG_NOMATCH)  
		{	
			break;
		}
		else if (0 == status)  
		{  			
			for(i = pmatch[0].rm_so;i<pmatch[0].rm_eo;++i)putchar(filedata[i + match_p]);  			 
			match_p = match_p + pmatch[0].rm_eo;
			printf("\n");
		}  
		
		 
		 
	}
	regfree(&reg); 
    return ;  
}  

void readOnly_file(char *fileName)
{
	int i=0;

	int length = 0;
	string line;

	ifstream myFile(fileName,ios_base::binary);
	
	myFile.seekg(0, myFile.end);
    length = myFile.tellg();
	myFile.seekg(0,myFile.beg);
    
	char *buff = new char[length];

	myFile.read(buff,length);
	
	ofstream ofile("tt",ios_base::binary);
	ofile.write(buff,length);
	
	delete[] buff;
	
}


int function () {
   ifstream ifs ("a.cap",  ifstream::binary);

  // get pointer to associated buffer object
   filebuf* pbuf = ifs.rdbuf();

  // get file size using buffer's members
   size_t size = pbuf->pubseekoff (0,ifs.end,ifs.in);
  pbuf->pubseekpos (0,ifs.in);

  // allocate memory to contain file data
  char* buffer=new char[size];

  // get file data
  pbuf->sgetn (buffer,size);

  ifs.close();

  // write content to stdout
   cout.write (buffer,size);

  delete[] buffer;

  return 0;
}


int cplusRegxMatch()
{
    
      if ( regex_match ("subject",  regex("(sub)(.*)") ))
         cout << "string literal matched\n";
    
      const char cstr[] = "subject";
       string s ("subject");
       regex e ("(sub)(.*)");
    
      if ( regex_match (s,e))
         cout << "string object matched\n";
    
      if (  regex_match ( s.begin(), s.end(), e ) )
         cout << "range matched\n";
    
       cmatch cm;    // same as  match_results<const char*> cm;
       regex_match (cstr,cm,e);
       cout << "string literal with " << cm.size() << " matches\n";
    
       smatch sm;    // same as  match_results<string::const_iterator> sm;
       regex_match (s,sm,e);
       cout << "string object with " << sm.size() << " matches\n";
    
       regex_match ( s.cbegin(), s.cend(), sm, e);
       cout << "range with " << sm.size() << " matches\n";
    
      // using explicit flags:
       regex_match ( cstr, cm, e,  regex_constants::match_default );
    
       cout << "the matches were: ";
      for (unsigned i=0; i<cm.size(); ++i) {
         cout << "[" << cm[i] << "] ";
      }
    
       cout <<  endl;
    
      return 0;
}

int main()
{
	//tt("./a.cap");
	//const char * pattern = "\"toNum\":\"([0-9]+)\"";  
	//regx("./a.cap",pattern);


    cplusRegxMatch();
	//writeOnly_file2("./2.txt");	
}
