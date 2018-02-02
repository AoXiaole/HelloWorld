#include<stdio.h>
#include <unistd.h>
#include<string.h>
#include <sys/stat.h>
#include <sys/types.h>
#define DIR_LEN 1024

// 目录格式为 /a/b/c  或 a/b/c ,  不带'/' 结束
static bool mkdir_r(char *pPath)
{
    char *p = NULL;
    if(access(pPath, F_OK) == 0) 
    {
        return true;
    }
    else  // 文件夹不存在
    {
        p = strrchr(pPath, '/');
        if(p == NULL || p == pPath)   // 最上层的目录了
        {
            if(mkdir(pPath, 0777) == 0)
            {
                return true;
            }
            else
            {
                return false;
            }
        }
        else
        {
            *p = 0; 
            if(mkdir_r(pPath) == true)  // 创建上级目录
            {
                *p = '/';
                if(mkdir(pPath, 0777) == 0)
                {
                    return true;
                }
                else
                {
                    return false;
                }
            }
            else
            {
                *p = '/';
                return false;
            }
        }
    }
    return false;
}

bool mkdir_p(const char *pPath)
{
    char   DirName[DIR_LEN + 1];  
    int   i; 
    int len = 0;  

    if(NULL == pPath)
    {
        return false;
    }
    
    strcpy(DirName, pPath);
    len = strlen(DirName);

    if(DirName[len-1] == '/')  
    {
        DirName[len-1] = 0;
    }
    
    return mkdir_r(DirName);  
    
}
