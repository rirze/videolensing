import sys
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph as pg
import numpy as np

def lens_start(vidlens):

    pg.setConfigOptions(imageAxisOrder='row-major')
    app = QtGui.QApplication([])
    win1 = pg.GraphicsLayoutWidget()
    win1.show()
    win2 = pg.GraphicsLayoutWidget()
    win2.show()

    view1 = win1.addViewBox()
    view1.setAspectLocked(True)
    view2 = win2.addViewBox()
    view2.setAspectLocked(True)

    view1.invertY()
    view2.invertY()

    h = vidlens.vid_height
    w = vidlens.vid_width

    unlensed = pg.ImageItem()
    lensed   = pg.ImageItem()

    view1.addItem(lensed)
    view2.addItem(unlensed)
    view1.setRange(QtCore.QRectF(0,0,w,h))
    view2.setRange(QtCore.QRectF(0,0,w,h))
        

    def update():
        vidlens.lensing_routine()

        unlensed.setImage(vidlens.unlensed)
        lensed.setImage(vidlens.lensedimg)

    timer = QtCore.QTimer()
    timer.timeout.connect(update)
    timer.start(0)
    
    sys.exit(app.exec_())
    
