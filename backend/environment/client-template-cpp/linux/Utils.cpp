#include "Utils.h"


bool SendBuffer(const std::vector<unsigned char>& outBuffer, int sock)
{
    return send(sock, outBuffer.data(), outBuffer.size(), 0) < 0;
}

bool ReadBuffer(std::vector<unsigned char>& inBuffer, int sock)
{
    return recv(sock, inBuffer.data(), BUFFERSIZE, 0) < 0;
}
