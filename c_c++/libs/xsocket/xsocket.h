#ifndef _XSOCKET_H_
#define _XSOCKET_H_
#include<string>
class Xsocket
{
private:
    int socketFd;
    struct timeval recvTimeOut;
    struct timeval sendTimeOut;
public:
    int *socketCounts;
    Xsocket(int _socketFd):socketFd(_socketFd){socketCounts = new int(1);}
    Xsocket(Xsocket &xsocket):socketFd(xsocket.socketFd),recvTimeOut(xsocket.recvTimeOut),sendTimeOut(xsocket.sendTimeOut),socketCounts(xsocket.socketCounts)
    {
        socketCounts=xsocket.socketCounts;
        (*socketCounts)++;
    }
	static 	std::string gethostbyname(std::string &url);
    int tcp_send(void *data,int len);
    int tcp_recv(void *data,int maxLen);
    void setTimeOut(int recvTimeOutMs,int sendTimeOutMs);
    ~Xsocket();
    
};

#endif
