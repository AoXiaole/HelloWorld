#include "tcp_server.h"  
#include <stdio.h>  
#include <unistd.h>
#include<string.h>
#include <stdlib.h>
using namespace std; 
 
tcp_server::tcp_server(int listen_port,int list_num) {  
  
        if(( socket_fd = socket(PF_INET,SOCK_STREAM,IPPROTO_TCP)) < 0 ){  
                throw "socket() failed";  
        }  
  
        memset(&myserver,0,sizeof(myserver));  
        myserver.sin_family = AF_INET;  
        myserver.sin_addr.s_addr = htonl(INADDR_ANY);  
        myserver.sin_port = htons(listen_port);  
  
        if( bind(socket_fd,(sockaddr*) &myserver,sizeof(myserver)) < 0 ) {  
                throw "bind() failed";  
        }  
  
        if( listen(socket_fd,10) < 0 ) {  
                throw "listen() failed";  
        }  
}  
  
int tcp_server::recv_msg() {  
  
        while( 1 ) {  
  
                socklen_t sin_size = sizeof(struct sockaddr_in);  
                if(( accept_fd = accept(socket_fd,(struct sockaddr*) &remote_addr,&sin_size)) == -1 )  
                {  
                        throw "Accept error!";  
                        continue;  
                }  
                printf("Received a connection from %s\n",(char*) inet_ntoa(remote_addr.sin_addr));  
  
                if( !fork() ) {  
                        char buffer[MAXSIZE];  
                        memset(buffer,0,MAXSIZE);  
                        if( ( read(accept_fd,buffer,MAXSIZE)) < 0 ) {  
                                throw("Read() error!");  
                        } else {  
                                printf("Received message: %s\n",buffer);  
                                break;  
                        }  
                        exit(0);  
                }  
                close(accept_fd);  
        }  
        return 0;  
}  


  
int main(int argc,char* argv[])  
{  
        tcp_server ts(atoi(argv[1]));  
        ts.recv_msg();  
        return 0;  
}  