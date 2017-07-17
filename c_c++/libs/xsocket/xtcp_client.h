#ifndef _XTCP_CLIENT_H_
#define _XTCP_CLIENT_H_

#include <unistd.h>  
#include <iostream>  
#include <sys/socket.h>  
#include <arpa/inet.h>  
#include <errno.h>  
class Xtcp_server_exception;
class Xtcp_client ;

class Xtcp_client_exception
{

public:
	enum EX_type{Xtcp_client_init_error};

	EX_type ex_type;
	std::string  ex_msg;
	Xtcp_client_exception(EX_type _ex_type,std::string _ex_msg):ex_type(_ex_type),ex_msg(_ex_msg){}
};

  
class Xtcp_client  
{  
private:  
        int socket_fd;  
        char message[4096];  
        struct sockaddr_in server_addr;  
  
public:  
	
        Xtcp_client(char* server_ip,int server_port);  
		int send(void *data,int len);
		int recv(void *data,int maxLen);
};
#endif
