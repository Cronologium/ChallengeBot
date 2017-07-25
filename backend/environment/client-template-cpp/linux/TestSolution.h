#pragma once
#include <vector>
#include <string>

#include "Solution.h"


class TestSolution : public Solution
{
public:
	TestSolution() { this->createShips(); }
	~TestSolution() {}
private:
	int count = 0;
	int i = 0;
	int j = 0;
	std::vector<std::string> ships;
	void createShips();

	std::vector<unsigned char> putShip(std::vector<unsigned char>& inBuffer) override;
	std::vector<unsigned char> shoot(std::vector<unsigned char>& inBuffer) override;
};
