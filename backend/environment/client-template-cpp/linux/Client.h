#pragma once
#include <vector>

#include "Utils.h"
#include "Solution.h"

#define SERVER_IP "127.0.0.1"
#define NO_SHIPS int(10)
#define $exit "$exit"


class Client
{
private:
	Solution* sol;
	std::string port;
	std::string user;
	int connSock;
public:
	Client(Solution* sol, std::string port, std::string user) : sol(sol), port(port), user(user) { this->conn(); }
	~Client() {}
	void run();
private:
	int conn();
};

