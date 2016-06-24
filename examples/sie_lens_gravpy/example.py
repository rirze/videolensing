# import matplotlib
# matplotlib.use('Qt5Agg')

from vidlens import VideoLens
from gravpy.models import SIE
from gravpy.gravpy import gravlens


lens = [SIE(2.0,0,0,0.,0,0.1)]
polargs = [[(0,0),2.0,10,42]]
size = 7.5; ratio = 720.0/1280 # resolution ratio
carargs = [[-size,size,0.5],[-size*ratio,size*ratio,0.5]] # lower bound, upper bound, initial spacing (two sets--for x and y axes)
sie_lens = gravlens(carargs, polargs, lens,show_plot=True, include_caustics=True,
                    recurse_depth=4, logging_level='warning')
sie_lens.run()
ui = 'cv'
vid_lens = VideoLens(lensinfo=sie_lens, pixelscale=0.011, draw_caustics=True, ui=ui)
vid_lens.run()
