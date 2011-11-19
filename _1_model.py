from PyQt4 import QtCore

from _1_roles import SERVER_NAME_ROLE, SERVER_LOAD_ROLE


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
