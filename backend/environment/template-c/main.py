import sys

from packages.package_manager import PackageManager


if len(sys.argv) < 4:
    print "Usage python", sys.argv[0], "<port> <username> <ID>"
elif __name__ == '__main__':
    package_manager = PackageManager()
    Api, Client = package_manager.fetch(int(sys.argv[3]))
    api = Api()
    client = Client(int(sys.argv[1]), sys.argv[2], api, './solution.so')
    client.main()

    # myClient = Client(Solution, int(sys.argv[1]), sys.argv[2])
    # while myClient.success is False:
    #    myClient = Client(Solution, int(sys.argv[1]), sys.argv[2])
    # myClient.hidden_main()
