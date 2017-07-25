#define _WIN32_WINNT 0x501

#include <iostream>
#include <future>
//#include <chrono>

#include "Client.h"


void Client::run()
{
	std::chrono::system_clock::time_point oneSecTimeout = std::chrono::system_clock::now() + std::chrono::seconds(1);
	std::vector<unsigned char> inBuffer;
	std::vector<unsigned char> outBuffer;

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
		}

		SendBuffer(outBuffer, connSock);*/
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
	// declarations
	WSADATA wsaData;
	struct addrinfo *addrresult = NULL, *ptr = NULL, hints;
	int iResult;
	std::string role;

	// definitions
	ZeroMemory(&hints, sizeof(hints));
	hints.ai_family = AF_UNSPEC;
	hints.ai_socktype = SOCK_STREAM;
	hints.ai_protocol = IPPROTO_TCP;
	connSock = INVALID_SOCKET;

	// initializing Winsock
	iResult = WSAStartup(MAKEWORD(2, 2), &wsaData);
	if (iResult != 0)
	{
		std::cout << "WSAStartup failed with error: " << iResult << std::endl;
		return iResult;
	}

	// resolve the server address and port
	iResult = getaddrinfo(SERVER_IP, this->port.c_str(), &hints, &addrresult);
	if (iResult != 0)
	{
		std::cout << "getaddrinfo failed with error: " << iResult << std::endl;
		WSACleanup();
		return iResult;
	}

	// attempting to connect to an address until one succeeds
#pragma warning(suppress: 4127) // while true is safe
	while (true)
	{
		for (ptr = addrresult; ptr != NULL; ptr = ptr->ai_next)
		{
			// creating a SOCKET for connecting to server
			connSock = socket(ptr->ai_family, ptr->ai_socktype, ptr->ai_protocol);
			if (INVALID_SOCKET == connSock)
			{
				std::cout << "socket failed with error: " << WSAGetLastError() << std::endl;
				WSACleanup();
				return WSAGetLastError();
			}

			// connecting to server
			iResult = connect(connSock, ptr->ai_addr, (int)ptr->ai_addrlen);
			if (SOCKET_ERROR == iResult)
			{
				closesocket(connSock);
				connSock = INVALID_SOCKET;
				continue;
			}
			break;
		}
		if (INVALID_SOCKET != connSock)
		{
			break;
		}
		// std::cout << "Unable to connect to server! - Trying again in 3 seconds." << std::endl;
		// Sleep(3000);
		Sleep(100);
	}
	freeaddrinfo(addrresult);

	// send username
	std::vector<unsigned char> buffer;
	buffer.resize(this->user.size());
	memcpy(buffer.data(), user.c_str(), this->user.size());
	SendBuffer(buffer, connSock);

	return 0;
}
