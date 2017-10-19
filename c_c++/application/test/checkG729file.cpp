#include<stdio.h>

#include <sys/types.h>
 #include <unistd.h>
 #include <string.h>
 
#include <sys/types.h>
       #include <sys/stat.h>
       #include <fcntl.h>
#define INVAILD_VALUE 0xffffffff
unsigned char g729_filler[] = {
        114, 170, 250, 103, 54, 211, 203, 194, 94, 64, 
        229, 127, 79, 96, 207, 82, 216, 110, 245, 81,
    };

unsigned int findMem(void *buff,unsigned int buffLen,void *findBin, unsigned int findBinLen)
{
    unsigned int i=0;
    for(i=0;i<buffLen-findBinLen+1;i++)
    {
        if(memcmp(buff + i,findBin,findBinLen) == 0)
        {
            return i;
        }
    }
    return INVAILD_VALUE;
}
unsigned int findMemRepeat(void *buff,int buffLen,void *findBin, int findBinLen,int *count)
{
    unsigned int pos=0;
    void *p=buff;
    int cc=0;
    *count=0;
    pos = findMem(buff,buffLen,findBin,findBinLen);
    if(pos != INVAILD_VALUE)
    {   
        cc++;
        p=buff+pos + findBinLen;
        buffLen = buffLen-pos-findBinLen;
        while(findMem(p,buffLen,findBin,findBinLen) == 0)
        {
            cc++;
            p += findBinLen;
            buffLen -= findBinLen;
        }
        *count = cc;
        return pos;
    }
    else
    {
        return INVAILD_VALUE;
    }
}
int main(int argv ,char *argc[])
{
    if(argv != 2)
    {
        write(2,"param error",strlen("param error"));
        return 1;
    }
    
    unsigned int  fileLen=0;
   
    char *fileName=argc[1];
    
    int fd=open(fileName,O_RDONLY);
    if(fd == -1)
    {
        perror("open file error");
        return 1;
    }

    fileLen=  lseek(fd,0,SEEK_END);
    lseek(fd,0,SEEK_SET);

    char *fileBuff = new char[fileLen+1];
    int ret=read(fd,fileBuff,fileLen);

    int count;
    unsigned int buffLen = fileLen;
    char *buff=fileBuff;

    unsigned int buff_off = 0;
    while(1)
    {
        buff_off = findMemRepeat(buff,buffLen,(void *)(g729_filler),sizeof(g729_filler),&count);
        if(buff_off != INVAILD_VALUE)
        {
            buff += buff_off;
            printf("offs : %d   repeat %d\n",buff - fileBuff,count);
   
            buff += sizeof(g729_filler) * count;
            buffLen = buffLen - (buff_off + sizeof(g729_filler) * count);
            
        }
        else
        {
            printf("fileLen = %d\n",fileLen);
            break;
        }
    }
    delete [] fileBuff;
    return 0;
    

   
}
