TOP=../../../
LIBS=$(TOP)/libs

CC=g++
TARGET= httpSwitch
INC=$(LIBS)/xsocket $(LIBS)/xstring
I_INC=$(foreach n,$(INC),-I $(n))
source=httpSwitch.cpp $(LIBS)/xsocket/xtcp_server.cpp $(LIBS)/xsocket/xtcp_client.cpp $(LIBS)/xstring/xstring.cpp
OBJ=$(source:%.cpp=%.o)
.PHNOY:all clean $(TARGET)

all:$(TARGET)

httpSwitch:$(OBJ)
	$(CC) -o $@ $(OBJ)  -lpthread
	
%.o:%.cpp
	$(CC) -c $< -o $@ $(I_INC)

clean:
	-rm $(TARGET) *.o -rf