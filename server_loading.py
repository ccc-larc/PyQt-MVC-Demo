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


class ServerProgressBarDelegate(QtGui.QStyledItemDelegate):
    def paint(self, painter, option, index):
        assert isinstance(painter, QtGui.QPainter)
        assert isinstance(option, QtGui.QStyleOptionViewItem)
        
        server = index.data(QtCore.Qt.UserRole).toPyObject()
        percent = int(server.load * 100.0)
        
        opts = QtGui.QStyleOptionProgressBarV2()
        opts.rect = option.rect
        opts.minimum = 0
        opts.maximum = 100
        opts.text = '%s: %d%%' % (server.name, percent)
        opts.textAlignment = QtCore.Qt.AlignCenter
        opts.textVisible = True
        opts.progress = percent
        QtGui.QApplication.style().drawControl(QtGui.QStyle.CE_ProgressBar, opts, painter)


class ServerLoadingSortProxyModel(QtGui.QSortFilterProxyModel):
    def lessThan(self, left, right):
        assert isinstance(left, QtCore.QModelIndex)
        assert isinstance(right, QtCore.QModelIndex)
        left_server = left.data(QtCore.Qt.UserRole).toPyObject()
        right_server = right.data(QtCore.Qt.UserRole).toPyObject()
        return (left_server.load < right_server.load)


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
    
    delegate = ServerProgressBarDelegate()
    view2 = QtGui.QListView()
    view2.setModel(model)
    view2.setItemDelegate(delegate)
    win.addWidget(view2)
    
    load_sort_proxy_model = ServerLoadingSortProxyModel()
    load_sort_proxy_model.setSourceModel(model)
    load_sort_proxy_model.sort(0, QtCore.Qt.DescendingOrder)
    view3 = QtGui.QListView()
    view3.setModel(load_sort_proxy_model)
    view3.setItemDelegate(delegate)
    win.addWidget(view3)
    
    win.show()
    return app.exec_()


if __name__ == '__main__':
    sys.exit(main())
