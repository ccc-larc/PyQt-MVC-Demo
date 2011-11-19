import random


class Server(object):
    def __init__(self, name):
        self.name = name
        self.load = random.randint(0, 100)
        self.active = True
    
    def update(self):
        if not self.active:
            return
        new_load = self.load + random.randint(-10, 10)
        self.load = sorted([0, new_load, 100])[1]


def console_display(servers):
    serv_list = []
    for serv in servers:
        serv_active = ('*' if serv.active else ' ')
        serv_list.append('[%s%s %3d%%]' % (serv.name, serv_active, serv.load))
    print('--'.join(serv_list))
