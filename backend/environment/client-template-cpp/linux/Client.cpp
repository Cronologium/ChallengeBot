#include <iostream>
#include <future>
//#include <chrono>
#include <unistd.h>
#include <string.h>

#include "Client.h"


void Client::run()
{
	//std::chrono::system_clock::time_point oneSecTimeout = std::chrono::system_clock::now() + std::chrono::seconds(1);
	std::vector<unsigned char> inBuffer;
	//std::vector<unsigned char> outBuffer;

	for (int i = 0; i < NO_SHIPS; i++)
	{
		inBuffer.clear();
		inBuffer.resize(BUFFERSIZE);
		ReadBuffer(inBuffer, connSock);
		
		if (std::string(inBuffer.begin(), inBuffer.begin() + sizeof($exit) - 1) == $exit)
		{
			std::cout << "Kicked :(" << std::endl;
			return;
		}
		
		/*outBuffer.clear();
		auto bindedFunction = std::bind(&Solution::putShip, this->sol, inBuffer);
		auto timedOperation = std::async(std::launch::async, bindedFunction, 0);
		if (std::future_status::ready == timedOperation.wait_until(oneSecTimeout))
		{
			outBuffer = timedOperation.get();
		}
		else
		{
			std::cout << "Timeout :(" << std::endl;
			return;
		}*/

		//SendBuffer(outBuffer, connSock);
        SendBuffer(this->sol->putShip(inBuffer), connSock);
	}

	inBuffer.clear();
	inBuffer.resize(BUFFERSIZE);
	ReadBuffer(inBuffer, connSock);

	while (std::string(inBuffer.begin(), inBuffer.begin() + sizeof($exit) - 1) != $exit)
	{
		/*outBuffer.clear();
		auto bindedFunction = std::bind(&Solution::shoot, this->sol, inBuffer);
		auto timedOperation = std::async(std::launch::async, bindedFunction, 0);
		if (std::future_status::ready == timedOperation.wait_until(oneSecTimeout))
		{
			outBuffer = timedOperation.get();
		}
		else
		{
			std::cout << "Timeout :(" << std::endl;
			return;
		}*/

		//SendBuffer(outBuffer, connSock);
		SendBuffer(this->sol->shoot(inBuffer), connSock);
		ReadBuffer(inBuffer, connSock);
	}
}

int Client::conn()
{
    struct sockaddr_in connStruct;
     
    // create socket
    connSock = socket(AF_INET , SOCK_STREAM , 0);
    if (connSock == -1)
    {
		std::cout << "Could not create socket" << std::endl;
    }
         
    connStruct.sin_addr.s_addr = inet_addr(SERVER_IP);
    connStruct.sin_family = AF_INET;
    connStruct.sin_port = htons(std::stoi(this->port));
 
    // connect to remote connStruct
    while (connect(connSock, (struct sockaddr *)&connStruct, sizeof(connStruct)) < 0)
    {
        sleep(0.1);
    }

	// send username
	std::vector<unsigned char> buffer;
	buffer.resize(this->user.size());
	memcpy(buffer.data(), user.c_str(), this->user.size());
	SendBuffer(buffer, connSock);

	return 0;
}
