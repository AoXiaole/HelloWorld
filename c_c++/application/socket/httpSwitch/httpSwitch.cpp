#include "xtcp_server.h"
#include "xtcp_client.h"
#include "xstring.h"
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
	
			struct hostent *host= NULL;
			host = gethostbyname("wxshglzjk.xyz");
			char   ip_str[32]={0};
			char 	*buff = new char[1024*1024];
            char 	*recvbuff = new char[1024*1024];
            int recvLen=0;
            
			int len=0;
			inet_ntop(host->h_addrtype, host->h_addr, ip_str, sizeof(ip_str));
            cout<<"newSocket :"<<newSocket<<endl;
			cout<<"[---> wxshglzjk.xyz ip:"<<ip_str<<" <---]"<<endl;
			Xtcp_client tcp_client(ip_str,80);
			while(1)
			{
				memset(buff,0,1024*1024);
                memset(recvbuff,0,1024*1024);
				if( ( len = read(newSocket,buff,MAXSIZE)) <= 0 ) 
				{  
			            break;  
			    } 
				else 
			    {  
			        //string str_buf(buff);
			      //  replace_all_distinct(str_buf,string("10.9.0.219"),string(ip_str));
			        cout<<newSocket<<"++++++++++read client data len = "<<len<<"++++++++++++++\n";
					len = replaceMem(buff,len,MAXSIZE,"10.9.0.219:8800",strlen("10.9.0.219:8800"),ip_str,strlen(ip_str));
                    
					cout<<newSocket<<"++++changed  data len =  "<<len<<"++buff+++++++\n"<<buff<<endl;
                        
                    
					len = tcp_client.send((void *)buff,len);
                    if(len > 0)
                    {
                        while(1)
                        {
                            cout<<newSocket<<"+++++++send to server buff success ++++\n";
                            memset(recvbuff,0,1024*1024);
                            recvLen = read(tcp_client.socket_fd,recvbuff,1024*1024);
                            if(recvLen > 0)
                            {
                                cout<<"------------recv server http data len = "<<recvLen<<"----------\n"<<recvbuff<<endl;
                                
                                if(send(newSocket,(void *)recvbuff,recvLen) == recvLen)
                                {
                                    cout<<"--------------send client success-------------\n";
                                }
                            }
                            else
                            {
                                break;
                            }
                       }
                    }
                    
				}
			}
			
		}
};


#if 0
    struct timeval timeout={3,0};//3s
   int ret=setsockopt(sock_fd,SOL_SOCKET,SO_SNDTIMEO,(const char*)&timeout,sizeof(timeout));
   int ret=setsockopt(sock_fd,SOL_SOCKET,SO_RCVTIMEO,(const char*)&timeout,sizeof(timeout));

   如果ret==0 则为成功,-1为失败,这时可以查看errno来判断失败原因
   int recvd=recv(sock_fd,buf,1024,0);
   if(recvd==-1&&errno==EAGAIN)
  {
       printf("timeout\n");
  }

#endif
int main()
{
#if 0	
    char buff[1024]={"123 3aot467ao r6y rtaoaoaoao1234"};
       int len = 0;
       cout<<strlen(buff);
    len = replaceMem(buff,strlen(buff),1024,"ao",2,"AOO",3);
    cout<<"  aflen :"<<len <<"\n"<<buff<<endl;
#else
  try{
        SwitchTcp SwitchTcp(8800,10);
        SwitchTcp.run();
    }
    catch(Xtcp_server_exception ex)
    {
        cout<<ex.ex_msg<<endl;
        return 0;
    }
    catch(Xtcp_client_exception ex)
    {
        cout<<ex.ex_msg<<endl;
        return 0;
    }
    
	while(1)
	{
		usleep(5000000);
	}
#endif
}
