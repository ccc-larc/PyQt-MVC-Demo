from PyQt4 import QtGui, QtCore

from _1_roles import SERVER_LOAD_ROLE


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
