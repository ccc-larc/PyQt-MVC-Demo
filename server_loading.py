import random
import sys

from PyQt4 import QtGui, QtCore


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


SERVER_NAME_ROLE = QtCore.Qt.UserRole
SERVER_LOAD_ROLE = QtCore.Qt.UserRole + 1

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
            return '%s: %s%%' % (server.name, server.load)
        
        elif role == SERVER_NAME_ROLE:
            return server.name
        
        elif role == SERVER_LOAD_ROLE:
            return server.load
        
        return QtCore.QVariant()
    
    def refreshLoading(self):
        for row in range(self.rowCount()):
            index = self.index(row)
            self.dataChanged.emit(index, index)


class ServerProgressBarDelegate(QtGui.QStyledItemDelegate):
    def paint(self, painter, option, index):
        assert isinstance(painter, QtGui.QPainter)
        assert isinstance(option, QtGui.QStyleOptionViewItem)
        
        server_name = index.data(SERVER_NAME_ROLE).toPyObject()
        server_load = index.data(SERVER_LOAD_ROLE).toPyObject()
        
        opts = QtGui.QStyleOptionProgressBarV2()
        opts.rect = option.rect
        opts.minimum = 0
        opts.maximum = 100
        opts.text = '%s: %d%%' % (server_name, server_load)
        opts.textAlignment = QtCore.Qt.AlignCenter
        opts.textVisible = True
        opts.progress = server_load
        QtGui.QApplication.style().drawControl(QtGui.QStyle.CE_ProgressBar, opts, painter)


class ServerLoadingSortProxyModel(QtGui.QSortFilterProxyModel):
    def lessThan(self, left, right):
        assert isinstance(left, QtCore.QModelIndex)
        assert isinstance(right, QtCore.QModelIndex)
        left_load = left.data(SERVER_LOAD_ROLE).toPyObject()
        right_load = right.data(SERVER_LOAD_ROLE).toPyObject()
        return (left_load < right_load)


class ServerLoadingFilterProxyModel(QtGui.QSortFilterProxyModel):
    def __init__(self, parent=None):
        super(ServerLoadingFilterProxyModel, self).__init__(parent)
        self._low_bound = 50
        self.setDynamicSortFilter(True)
    
    def filterAcceptsRow(self, source_row, source_parent):
        assert isinstance(source_row, int)
        assert isinstance(source_parent, QtCore.QModelIndex)
        source_index = self.sourceModel().index(source_row, 0)
        server_load = source_index.data(SERVER_LOAD_ROLE).toPyObject()
        return (server_load >= self._low_bound)
    
    def lowBound(self):
        return self._low_bound
    
    def setLowBound(self, low_bound):
        assert 0 <= low_bound <= 100
        self._low_bound = low_bound
        self.filterChanged()


def console_display(servers):
    serv_list = []
    for serv in servers:
        serv_active = ('*' if serv.active else ' ')
        serv_list.append('[%s%s %3d%%]' % (serv.name, serv_active, serv.load))
    print('--'.join(serv_list))


def main():
    print('Python %s' % sys.version)
    
    servers = [Server('A'), Server('B'), Server('C')]
    
    app = QtGui.QApplication(sys.argv)
    win = QtGui.QSplitter()
    
    model = ServerModel(servers)
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
    load_sort_proxy_model.setDynamicSortFilter(True)
    load_sort_proxy_model.sort(0, QtCore.Qt.DescendingOrder)
    view3 = QtGui.QListView()
    view3.setModel(load_sort_proxy_model)
    view3.setItemDelegate(delegate)
    win.addWidget(view3)
    
    load_filter_proxy_model = ServerLoadingFilterProxyModel()
    load_filter_proxy_model.setSourceModel(load_sort_proxy_model)
    view4 = QtGui.QListView()
    view4.setModel(load_filter_proxy_model)
    view4.setItemDelegate(delegate)
    
    slider = QtGui.QSlider(QtCore.Qt.Horizontal)
    slider.setRange(0, 100)
    slider.setTickInterval(10)
    slider.setTickPosition(QtGui.QSlider.TicksAbove)
    slider.setValue(load_filter_proxy_model.lowBound())
    slider.valueChanged.connect(load_filter_proxy_model.setLowBound)
    
    layout4 = QtGui.QVBoxLayout()
    layout4.addWidget(view4)
    layout4.addWidget(slider)
    
    widget4 = QtGui.QWidget()
    widget4.setLayout(layout4)
    win.addWidget(widget4)
    
    win.show()
    
    def _update_servers():
        for serv in servers:
            serv.update()
        console_display(servers)
        model.refreshLoading()
        
    timer = QtCore.QTimer()
    timer.setInterval(250)
    timer.timeout.connect(_update_servers)
    timer.start(250)
    
    return app.exec_()


if __name__ == '__main__':
    sys.exit(main())
