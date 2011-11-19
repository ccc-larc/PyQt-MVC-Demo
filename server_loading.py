import sys

from PyQt4 import QtGui, QtCore

from _0_server import Server, console_display
from _1_model import ServerModel
from _2_progress_bar_delegate import ServerProgressBarDelegate
from _3_sort_proxy_model import ServerLoadingSortProxyModel
from _4_filter_proxy_model import ServerLoadingFilterProxyModel


def main():
    print('Python %s' % sys.version)
    
    servers = [Server('A'), Server('B'), Server('C')]
    
    app = QtGui.QApplication(sys.argv)
    model = ServerModel(servers)
    
    view_control = [True, False, False, False]
    show_view1 = view_control[0]
    show_view2 = show_view1 & view_control[1]
    show_view3 = show_view2 & view_control[2]
    show_view4 = show_view3 & view_control[3]
    
    if show_view1:
        win = QtGui.QSplitter()
        
        view1 = QtGui.QListView()
        view1.setModel(model)
        win.addWidget(view1)
    
    if show_view2:
        delegate = ServerProgressBarDelegate()
        view2 = QtGui.QListView()
        view2.setModel(model)
        view2.setItemDelegate(delegate)
        win.addWidget(view2)
    
    if show_view3:
        load_sort_proxy_model = ServerLoadingSortProxyModel()
        load_sort_proxy_model.setSourceModel(model)
        load_sort_proxy_model.setDynamicSortFilter(True)
        load_sort_proxy_model.sort(0, QtCore.Qt.DescendingOrder)
        view3 = QtGui.QListView()
        view3.setModel(load_sort_proxy_model)
        view3.setItemDelegate(delegate)
        win.addWidget(view3)
    
    if show_view4:
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
    
    if show_view1:
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
