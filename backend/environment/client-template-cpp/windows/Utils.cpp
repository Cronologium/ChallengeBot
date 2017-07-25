#include "Utils.h"


bool SendBuffer(const std::vector<unsigned char>& outBuffer, SOCKET sock)
{
	DWORD bytesSent = 0;
	while (bytesSent != outBuffer.size())
	{
		int res = send(sock, (char*)&outBuffer[bytesSent], (int)outBuffer.size() - bytesSent, 0);
		if (res == SOCKET_ERROR || res == 0)
			return false;
		bytesSent += res;
	}

	return true;
}

bool ReadBuffer(std::vector<unsigned char>& inBuffer, SOCKET sock)
{
	DWORD bytesRead = 0;
	/*while (bytesRead != BUFFERSIZE)
	{
		int res = recv(sock, (char*)&inBuffer[bytesRead], (int)BUFFERSIZE - bytesRead, NULL);
		if (res == SOCKET_ERROR)
			return false;
		if (res == 0)
			break;
		bytesRead += res;
	};*/

	int res = recv(sock, (char*)&inBuffer[bytesRead], (int)BUFFERSIZE - bytesRead, 0);
	if (res == SOCKET_ERROR)
		return false;

	return true;
}
