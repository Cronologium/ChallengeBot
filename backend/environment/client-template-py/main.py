import sys

from client.client import Client
try:
    from solution.solution import Solution
except ImportError:
    from solution.emptySolution import Solution
except NameError:
    from solution.emptySolution import Solution  # fucking temporary workaround

if len(sys.argv) < 3:
    print "Please specify a port and a username"
elif __name__ == '__main__':
    myClient = Client(Solution, int(sys.argv[1]), sys.argv[2])
    while myClient.success is False:
        myClient = Client(Solution, int(sys.argv[1]), sys.argv[2])
    myClient.hidden_main()
