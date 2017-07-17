#include "xstring.h"
using namespace std;

/*string 分隔函数 
 *@str 需要被分隔的字符串
 *@pattern 分隔符集合，可以是多个字符
 *return 分隔后的vector向量表*/
vector<string> split( string &str, string &pattern)
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


/*将str中的old_str 替换为 new_str ,替换后的结果也参与替换*/
string& replace_all(string& str, const string&  old_str, const  string&  new_str)     
{     
    string::size_type old_len = old_str.length();
    
    while(true)   
    {     
        string::size_type   pos(0);     
        
        if((pos=str.find(old_str)) != string::npos)     
        { 
            str.replace(pos, old_len, new_str);  
        }   
        else  
        { 
            break;
        }
    }     
    return   str;     
}     


/*将str中的所有old_str 替换为 new_str */
string&   replace_all_distinct(string&   str, const  string&  old_str, const   string&   new_str)     
{     
    string::size_type old_len = old_str.length();

    for(string::size_type   pos(0);   pos!=string::npos;   pos+=new_str.length())  
    {     
        if((pos=str.find(old_str,pos)) != string::npos)     
        { 
            str.replace(pos,old_len,new_str);  
        }   
        else  
        { 
            break; 
        }    
    }     
    return   str;     
}     



int replaceMem(char *srcdata,int srcLen,int srcMaxLen,char *oldData,int old_len,char *newData,int new_len)
{
    int ret=0;
    unsigned int i=0;
    unsigned copy_len=0;
    char * src_p = srcdata;
    char * new_p = NULL; 
    int count=0;
    
    char *buff = new char[srcMaxLen];
    if (buff == NULL)
        return -1;
    
    new_p = buff;
   
    i=0;
    while(((src_p + i) != (srcdata + srcLen)))
    {
        if(memcmp(src_p+i,oldData,old_len) == 0)
        {
           
            if((new_p + i + new_len) > (buff + srcMaxLen))
            {
                ret=-1;
                break;
            } 
            count++;
            memcpy(new_p,src_p,i);
            memcpy(new_p+i,newData,new_len);
            new_p += i + new_len;
            
       
            src_p += i + old_len;
            i=0;
        }
        else
            i++;
    }
    
    if((new_p+i) > (buff + srcMaxLen))
    {
        ret=-1;
    }    
    else
    {
        memcpy(new_p,src_p,i);
        
    }

    memcpy(srcdata,buff,srcMaxLen);
    delete buff;

    if(ret == -1)
        return -1;
    else
        return srcLen + (new_len-old_len)*count; 

}