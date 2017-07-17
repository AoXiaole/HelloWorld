#ifndef _XSTRING_H_
#define _XSTRING_H_
#include<string>
#include<string.h>
#include <vector>

std::vector<std::string> split(std::string &str, std::string &pattern);
std::string& replace_all(std::string& str, const std::string&  old_value, const  std::string&  new_value);
std::string&   replace_all_distinct(std::string&   str, const  std::string&  old_value, const   std::string&   new_value); 
int replaceMem(char *srcdata,int srcLen,int srcMaxLen,char *oldData,int old_len,char *newData,int new_len);

#endif
