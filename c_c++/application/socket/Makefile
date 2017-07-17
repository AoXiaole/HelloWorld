CC=g++
TARGET= tcp_server tcp_client
.PHNOY:all clean $(TARGET)

all:$(TARGET)

tcp_client:tcp_client.cpp tcp_client.h
	$(CC) -o $@ $^
tcp_server:tcp_server.cpp tcp_server.h
	$(CC) -o $@ $^
clean:
	-rm $(TARGET) *.o