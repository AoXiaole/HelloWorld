#ifndef _XTCP_SERVER_H__
#define _XTCP_SERVER_H__

#include <unistd.h>  
#include <iostream>  
#include <sys/socket.h>  
#include <arpa/inet.h>  
#include<string>
#include <pthread.h>

#define MAXSIZE 1024*1024 
class Xtcp_server;
class Xtcp_server_exception;
class Xtcp_server_threadParam;

class Xtcp_server_exception
{

public:
	enum EX_type{Xtcp_server_init_error};

	EX_type ex_type;
	std::string  ex_msg;
	Xtcp_server_exception(EX_type _ex_type,std::string _ex_msg):ex_type(_ex_type),ex_msg(_ex_msg){}
};

class Xtcp_server_threadParam
{
public:
	Xtcp_server *tcp_server;
	int sockfd;
	Xtcp_server_threadParam(Xtcp_server *_tcp_server,int _sockfd):tcp_server(_tcp_server),sockfd(_sockfd){}
	
};


class Xtcp_server  
{  
private:  
        int socket_fd;  
        sockaddr_in myserver;  
        int running;
		int listen_port;
		int listen_num;
		pthread_t pAccpetThread;
		
	
public:  
        Xtcp_server(int listen_port,int listen_num=10);  
		int run();
		int stop();
		static void* accpetThread(void *arg);
		static void* newClientThread(void *arg);
		virtual int newClient(int newSocket);

        int send(int socketfd,void *data,int len);
        int recv(int socketfd,void *data,int maxLen);
		
};


#endif
