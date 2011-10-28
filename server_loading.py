import random
import sys
import time

from PyQt4 import QtGui, QtCore


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


class ServerModel(QtCore.QAbstractListModel):
    def __init__(self, servers, parent=None):
        super(ServerModel, self).__init__(parent)
        self._servers = servers
    
    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self._servers)
    
    def data(self, index, role=QtCore.Qt.DisplayRole):
        if not index.isValid():
            return QtCore.QVariant()
        
        row = index.row()
        server = self._servers[row]
        if role == QtCore.Qt.DisplayRole:
            return '%s: %s%%' % (server.name, int(server.load * 100.0))
        
        elif role == QtCore.Qt.UserRole:
            return server
        
        return QtCore.QVariant()
    

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
    
    app = QtGui.QApplication(sys.argv)
    win = QtGui.QSplitter()
    
    model = ServerModel(server_holder.servers)
    view1 = QtGui.QListView()
    view1.setModel(model)
    win.addWidget(view1)
    
    win.show()
    return app.exec_()


if __name__ == '__main__':
    sys.exit(main())
