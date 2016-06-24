import matplotlib
matplotlib.use('Qt5Agg')

from vidlens import VideoLens
from gravpy.models import nfw
from gravpy.gravpy import gravlens

modelargs = [nfw(4,0,0,0.2,0,0.5)]
polargs = [[(0,0),4.0,10,42]]
size = 10; ratio = 720.0/1280
carargs = [[-size,size,0.5],[-size*ratio,size*ratio,0.5]] # lower bound, upper bound, initial spacing (two sets--for x and y axes)
nfw_lens = gravlens(carargs, polargs, modelargs ,show_plot=True, include_caustics=True,
                    recurse_depth=4, logging_level='warning')

vid_lens = VideoLens(lensinfo=nfw_lens, draw_caustics=True, pixelscale=0.011, ui='qt')
vid_lens.run()
