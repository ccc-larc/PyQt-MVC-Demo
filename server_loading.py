import random
import sys
import time


class Server(object):
    def __init__(self, name):
        self.name = name
        self.load = random.uniform(0.0, 1.0)
        self.active = True
    
    def update(self):
        if not self.active:
            return
        new_load = self.load + random.uniform(-0.1, 0.1)
        self.load = sorted([0.0, new_load, 1.0])[1]


class ServerHolder(object):
    def __init__(self):
        self.servers = []
    
    def add_server(self, name):
        self.servers.append(Server(name))
    
    def update(self):
        for serv in self.servers:
            serv.update()


def console_display(servers):
    serv_list = []
    for serv in servers:
        serv_load = '%3d%%' % int(serv.load * 100.0)
        serv_active = ('*' if serv.active else ' ')
        serv_list.append('[%s%s %s]' % (serv.name, serv_active, serv_load))
    print('--'.join(serv_list))


def main():
    print('Python %s' % sys.version)
    
    server_holder = ServerHolder()
    server_holder.add_server('A')
    server_holder.add_server('B')
    server_holder.add_server('C')
    
    while True:
        server_holder.update()
        console_display(server_holder.servers)
        time.sleep(1)
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
