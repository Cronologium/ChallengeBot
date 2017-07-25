#pragma once
#include <vector>
#include <string>

#include <WinSock2.h>
#include <Windows.h>
#include <ws2tcpip.h>

#pragma comment (lib, "Ws2_32.lib")

#define BUFFERSIZE 512


bool SendBuffer(const std::vector<unsigned char>& outBuffer, SOCKET sock);
bool ReadBuffer(std::vector<unsigned char>& inBuffer, SOCKET sock);
