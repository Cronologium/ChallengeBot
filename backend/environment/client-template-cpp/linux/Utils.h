#pragma once
#include <vector>
#include <string>

#include <sys/socket.h>
#include <arpa/inet.h> //inet_addr

#define BUFFERSIZE 512


bool SendBuffer(const std::vector<unsigned char>& outBuffer, int sock);
bool ReadBuffer(std::vector<unsigned char>& inBuffer, int sock);
