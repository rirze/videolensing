from vidlens import VideoLens
from gravpy.models import SIE
from gravpy import gravlens

lens = [SIE(1.5,0,0,0.5,0,0.1)]
ppolargs2 = [[(0,0),1.5,10,42]]
size = 10; ratio = 1280.0/960
pcarargs = [[-size,size,0.5],[-size*ratio,size*ratio,0.5]] # lower bound, upper bound, initial spacing (two sets--for x and y axes)

vid_lens = VideoLens(lensinfo=gravlens(pcarargs, ppolargs2, lens))
vid_lens.save_interpolation('1280x960-SIE1.5','npy')
# vid_lens.run()
