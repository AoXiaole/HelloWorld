#include"xsocket.h"
using namespace std;
string Xsocket::gethostbyname(string &url)
{
    string ip;
    char ip_str[32]={0};
    struct hostent *host= NULL;
	host = ::gethostbyname(url.c_str());
    if(host == NULL)
        return ip;
    inet_ntop(host->h_addrtype, host->h_addr, ip_str, sizeof(ip_str));
    ip=ip_str;
    return ip;
    
}

Xsocket::Xsocket(Xsocket &xsocket)
{
    
}
Xsocket::~Xsocket()
{
    if(*socketCounts == 1)
    {
        delete socketCounts;
        close(socketFd);
    }
    else
    {
        (*socketCounts)--;
    }
}