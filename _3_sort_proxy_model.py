from PyQt4 import QtGui, QtCore

from _1_roles import SERVER_LOAD_ROLE


class ServerLoadingSortProxyModel(QtGui.QSortFilterProxyModel):
    def lessThan(self, left, right):
        assert isinstance(left, QtCore.QModelIndex)
        assert isinstance(right, QtCore.QModelIndex)
        left_load = left.data(SERVER_LOAD_ROLE).toPyObject()
        right_load = right.data(SERVER_LOAD_ROLE).toPyObject()
        return (left_load < right_load)
