#include "xtcp_server.h"
#include<vector>
#include<stdio.h>
#include<string.h>
Xtcp_server::Xtcp_server(int listen_port,int listen_num)
{
	running=0;
	
	if(( socket_fd = socket(PF_INET,SOCK_STREAM,IPPROTO_TCP)) < 0 ){  
                throw Xtcp_server_exception(Xtcp_server_exception::Xtcp_server_init_error,"socketinit failed");  
        }  
  
        memset(&myserver,0,sizeof(myserver));
        myserver.sin_family = AF_INET;  
        myserver.sin_addr.s_addr = htonl(INADDR_ANY);  
        myserver.sin_port = htons(listen_port);  
  
        if( bind(socket_fd,(sockaddr*) &myserver,sizeof(myserver)) < 0 ) {  
                throw Xtcp_server_exception(Xtcp_server_exception::Xtcp_server_init_error,"bind failed");  
        }  
  
        if( listen(socket_fd,listen_num) < 0 ) {  
               throw Xtcp_server_exception(Xtcp_server_exception::Xtcp_server_init_error,"listen() failed");  
        }  
}
int Xtcp_server::run()
{
	running=1;
	Xtcp_server_threadParam *threadParam_accpet = new Xtcp_server_threadParam(this,0);
	pthread_create(&pAccpetThread,NULL,accpetThread,(void *)threadParam_accpet);
	return 1;
}
int Xtcp_server::stop()
{
	running=0;
	return 0;
}

void* Xtcp_server::accpetThread(void *arg)
{
	Xtcp_server_threadParam *threadParam_accpet = (Xtcp_server_threadParam *)arg;
	
	socklen_t sin_size = sizeof(struct sockaddr_in);
	int accept_fd;
	sockaddr_in remote_addr;
	pthread_t pNewClientThread;
	
	while(threadParam_accpet->tcp_server->running)
	{
		if(( accept_fd = accept(threadParam_accpet->tcp_server->socket_fd,(struct sockaddr*) &remote_addr,&sin_size)) == -1 )  
	    {  
	           ;
	    }  
	    else
		{	
//			printf("Received a connection from %s\n",(char*) inet_ntoa(remote_addr.sin_addr));  
			
			Xtcp_server_threadParam *threadParam_newClient = new Xtcp_server_threadParam(threadParam_accpet->tcp_server,accept_fd);
			pthread_create(&pNewClientThread,NULL,newClientThread,(void *)threadParam_newClient);
	   	}

	}
	delete threadParam_accpet;
	
   
	return NULL;
	
}

void * Xtcp_server::newClientThread(void *arg)
{

//	vector<char> msgBuff;
	
	Xtcp_server_threadParam *threadParam_newClient = (Xtcp_server_threadParam *)arg;

//	while(tcp_server_threadParam.tcp_server->running)
	int newsocket = threadParam_newClient->sockfd;
//	printf("newClientThread:have new accpet\n");
	threadParam_newClient->tcp_server->newClient(newsocket);

	 
	close(newsocket);
	delete threadParam_newClient;

        return NULL;  
}
int Xtcp_server::newClient(int newSocket)
{
	
    char *buffer = new char[MAXSIZE];  
    memset(buffer,0,MAXSIZE);  
    if( ( read(newSocket,buffer,MAXSIZE)) < 0 ) {  
            throw("Read() error!");  
    } else {  
    		printf("%s",buffer);
            
            
    }                
     delete buffer;
	 return 0;
}
int Xtcp_server::send(int socketfd,void *data,int len)
{
    return ::send(socketfd,(char *)data,len,0 );
}

int Xtcp_server::recv(int socketfd,void *data,int maxLen)
{
    int len = 0;
    int totalLen=0;
    char temp[1024] = {0};
    struct timeval timeout={5,0};//5s
    int ret=setsockopt(socket_fd,SOL_SOCKET,SO_RCVTIMEO,(const char*)&timeout,sizeof(timeout));
    
    while(1)
    {
        memset(temp,0,sizeof(temp));
    	if( ( len = read(socketfd,(void *)temp,sizeof(temp))) <= 0 ) 
    	{  
               break;  
        } 
    	else 
        {  
        	memcpy(data+totalLen,temp,len);
            totalLen +=len;
        }
    }
    return totalLen;
}


