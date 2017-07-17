TOP=../../../
LIBS=$(TOP)/libs

CC=g++
TARGET= httpSwitch
INC=$(LIBS)/xsocket
source=httpSwitch.cpp $(LIBS)/xsocket/xtcp_server.cpp $(LIBS)/xsocket/xtcp_client.cpp

.PHNOY:all clean $(TARGET)

all:$(TARGET)

httpSwitch:$(source)
	$(CC) -o $@ $^ -I $(INC) -lpthread

clean:
	-rm $(TARGET) *.o