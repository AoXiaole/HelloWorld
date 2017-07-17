#include "xtcp_client.h"
#include<string.h>
Xtcp_client::Xtcp_client(char* server_ip,int server_port)  
{  
       if( (socket_fd = socket(AF_INET,SOCK_STREAM,0)) < 0 ) {  
                throw Xtcp_client_exception(Xtcp_client_exception::Xtcp_client_init_error,"socket init error");
        }  


       struct timeval timeout={5,0};//3s
        int ret=setsockopt(socket_fd,SOL_SOCKET,SO_RCVTIMEO,(const char*)&timeout,sizeof(timeout));
        memset(&server_addr,0,sizeof(server_addr));  
        server_addr.sin_family = AF_INET;  
        server_addr.sin_port = htons(server_port);  
  
        if( inet_pton(AF_INET,server_ip,&server_addr.sin_addr) <=0 ) {  
                throw Xtcp_client_exception(Xtcp_client_exception::Xtcp_client_init_error,"inet_pton error");  
        }  
  
        if( connect(socket_fd,(struct sockaddr*)&server_addr,sizeof(server_addr))<0) {  
                throw Xtcp_client_exception(Xtcp_client_exception::Xtcp_client_init_error,"connect error");  
        }  
  
 
        
  
}
int Xtcp_client::send(void *data,int len)
{
	return ::send(socket_fd,(char *)data,len,0 );
}

int Xtcp_client::recv(void *data,int maxLen)
{
    int len = 0;
    int totalLen=0;
    char temp[1024] = {0};
    struct timeval timeout={5,0};//3s
    int ret=setsockopt(socket_fd,SOL_SOCKET,SO_RCVTIMEO,(const char*)&timeout,sizeof(timeout));
    
    while(1)
    {
        memset(temp,0,sizeof(temp));
    	if((len = read(socket_fd,(void *)temp,sizeof(temp))) <= 0) 
    	{  
               break;  
        } 
    	else 
        {  
        	memcpy(data+totalLen,(void *)temp,len);
            totalLen +=len;
        }
    }
    return totalLen;
}


