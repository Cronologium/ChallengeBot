#pragma once
#include <vector>


class Solution
{
public:
	Solution() {}
	~Solution() {}

	std::vector<unsigned char> outBuffer;
	virtual std::vector<unsigned char> putShip(std::vector<unsigned char>& inBuffer) = 0;
	virtual std::vector<unsigned char> shoot(std::vector<unsigned char>& inBuffer) = 0;
};
