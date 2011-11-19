from PyQt4 import QtGui, QtCore

from _1_roles import SERVER_NAME_ROLE, SERVER_LOAD_ROLE


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
