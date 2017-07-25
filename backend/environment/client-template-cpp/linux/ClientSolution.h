#pragma once
#include <vector>
#include <string>

#include "Solution.h"


class ClientSolution : public Solution
{
public:
	// mandatory
	ClientSolution();
	~ClientSolution();
private:
	// use them only if you need
	int count = 0;
	int i = 0;
	int j = 0;
	std::vector<std::string> ships;
	void createShips();

	// mandatory
	std::vector<unsigned char> putShip(std::vector<unsigned char>& inBuffer) override;
	std::vector<unsigned char> shoot(std::vector<unsigned char>& inBuffer) override;
};
