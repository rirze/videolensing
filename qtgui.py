import sys
from qtpy import QtCore
from qtpy import QtWidgets
from qtpy import QtGui
from qtpy.QtCore import pyqtSignal

class ImageViewer(QtWidgets.QWidget):
    def __init__(self, title, parent = None):
        super(ImageViewer, self).__init__(parent)
        self.image = QtGui.QImage()
        self.setAttribute(QtCore.Qt.WA_OpaquePaintEvent)
        self.setWindowTitle(title)
 
    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.drawImage(0,0, self.image)
        self.image = QtGui.QImage()
 
    @QtCore.pyqtSlot(QtGui.QImage)
    def setImage(self, image):
        if image.isNull():
            print("Viewer Dropped frame!")
 
        self.image = image
        if image.size() != self.size():
            self.setFixedSize(image.size())
        self.update()

class ShowVideo(QtCore.QObject):
 
    VideoSignal1 = QtCore.pyqtSignal(QtGui.QImage)
    VideoSignal2 = QtCore.pyqtSignal(QtGui.QImage)
    
    def __init__(self, vidlens, parent = None):
        super(ShowVideo, self).__init__(parent)
        self.vidlens = vidlens
 
    @QtCore.pyqtSlot()
    def startVideo(self):
 
        run_video = True
        while run_video:
            self.vidlens.lensing_routine()
            
            lensedimage = QtGui.QImage(self.vidlens.lensedimg.copy(),
                                    self.vidlens.width,
                                    self.vidlens.height,
                                    QtGui.QImage.Format_RGB888)
            unlensed    = QtGui.QImage(self.vidlens.unlensed.copy(),
                                       self.vidlens.width,
                                       self.vidlens.height,
                                       QtGui.QImage.Format_RGB888)
            
            self.VideoSignal1.emit(lensedimage)
            self.VideoSignal2.emit(unlensed)
    
def lens_start(vidlens):

    app = QtWidgets.QApplication(sys.argv)
    thread = QtCore.QThread()
    thread.start()
    vid = ShowVideo(vidlens)
    vid.moveToThread(thread)
    lensed_view = ImageViewer('Lensed Video')
    unlensed_view = ImageViewer('Unlensed Video')

    
    vid.VideoSignal1.connect(lensed_view.setImage)
    vid.VideoSignal2.connect(unlensed_view.setImage)
 
    # Button to start/stop the videocapture:
    vertical_layout = QtWidgets.QVBoxLayout()
 
    push_button = QtWidgets.QPushButton('Start')
    push_button.clicked.connect(vid.startVideo)

    def end_function():
        app.closeAllWindows()
        thread.quit()
        
    end_button  = QtWidgets.QPushButton('End')
    end_button.clicked.connect(end_function)
    

    vertical_layout.addWidget(push_button)
    vertical_layout.addWidget(end_button)

    layout_widget = QtWidgets.QWidget()
    layout_widget.setLayout(vertical_layout)
    
    layout_widget.setWindowTitle('Control Panel')
    layout_widget.show()

    lensed_view.show()
    unlensed_view.show()
    
    # thread.quit()
    sys.exit(app.exec_())









