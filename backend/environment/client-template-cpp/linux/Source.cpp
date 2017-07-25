#include <iostream>

#include "Client.h"
#include "ClientSolution.h"


int main(int argc, char* argv[])
{
	if (argc < 2) {
		std::cout << "Please specify a port and a username" << std::endl;
		return 1;
	}
	
	Solution* sol = new ClientSolution{};
	Client myClient{ sol, std::string(argv[1]), std::string(argv[2]) };
	myClient.run();
	delete sol;

	return 0;
}
