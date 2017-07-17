#include "xtcp_server.h"
#include "xtcp_client.h"
#include <unistd.h>
#include <netdb.h>
#include <sys/socket.h> 
#include <stdio.h>
#include<string.h>
       extern int h_errno;


using namespace std;


class SwitchTcp:public Xtcp_server
{
public:
	SwitchTcp(int listen_port,int listen_num=10):Xtcp_server(listen_port,listen_num){}
		int newClient(int newSocket){
			printf("newClient:");
			struct hostent *host= NULL;
			host = gethostbyname("wxshglzjk.xyz");
			char   ip_str[32]={0};
			char 	*buff = new char[1024*1024];
			int len=0;
			inet_ntop(host->h_addrtype, host->h_addr, ip_str, sizeof(ip_str));
			cout<<" wxshglzjk.xyz ip:"<<ip_str<<endl;
			Xtcp_client tcp_client(ip_str,80);
			while(1)
			{
				memset(buff,0,1024*1024);
				if( ( len = read(newSocket,buff,MAXSIZE)) <= 0 ) 
				{  
			            break;  
			    } 
				else 
			    {  
			    
					cout<<"bufflen:"<<len<<endl;
					cout<<"buff:"<<buff<<endl;
					tcp_client.send(buff,len);
				}
			}
			
		}
};

int main()
{
	SwitchTcp SwitchTcp(8000,10);
	SwitchTcp.run();
	while(1)
	{
		usleep(5000000);
	}
}
