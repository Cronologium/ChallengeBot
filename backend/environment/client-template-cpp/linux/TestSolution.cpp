#include "TestSolution.h"

#include <string.h>


std::vector<unsigned char> TestSolution::putShip(std::vector<unsigned char>& inBuffer)
{
	inBuffer;
	outBuffer.resize(ships[count].size());
	memcpy(outBuffer.data(), ships[count].c_str(), ships[count].size());
	count++;

	return outBuffer;
}

std::vector<unsigned char> TestSolution::shoot(std::vector<unsigned char>& inBuffer)
{
	inBuffer;
	std::string s("shoot " + std::to_string(i) + " " + std::to_string(j));
	outBuffer.resize(s.size());
	memcpy(outBuffer.data(), s.c_str(), s.size());
	if (j == 9)
	{
		j = 0;
		i++;
	}
	else
	{
		j++;
	}

	return outBuffer;
}


void TestSolution::createShips()
{
	ships.push_back("ship 0 0 0 0");
	ships.push_back("ship 0 1 0 1");
	ships.push_back("ship 3 0 3 3");
	ships.push_back("ship 0 2 0 2");
	ships.push_back("ship 0 3 0 3");
	ships.push_back("ship 2 3 2 5");
	ships.push_back("ship 1 0 1 1");
	ships.push_back("ship 1 2 1 3");
	ships.push_back("ship 1 4 1 5");
	ships.push_back("ship 2 0 2 2");	
}
