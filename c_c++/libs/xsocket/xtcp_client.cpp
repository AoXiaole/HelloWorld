#include "xtcp_client.h"
#include<string.h>
Xtcp_client::Xtcp_client(char* server_ip,int server_port)  
{  
       if( (socket_fd = socket(AF_INET,SOCK_STREAM,0)) < 0 ) {  
                throw Xtcp_client_exception(Xtcp_client_exception::Xtcp_client_init_error,"socket init error");
        }  
    
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
	if( ( read(socket_fd,data,maxLen)) < 0 ) 
	{  
           return -1;  
    } 
	else 
    {  
    		return 0;
    }
}


