from vidlens import VideoLens
from gravpy.models import SIE


lens = [SIE(2.0,0,0,0,0,0.1)]
ppolargs2 = [[(0,0),2.0,10,42]]
size = 10; ratio = 720.0/1280
pcarargs = [[-size,size,0.5],[-size*ratio,size*ratio,0.5]] # lower bound, upper bound, initial spacing (two sets--for x and y axes)

vid_lens = VideoLens(lensinfo=[lens,pcarargs,ppolargs2])
vid_lens.save_interpolation(['../sie_lens/1280x720-SIE2.0'],'npy')
# vid_lens.run()
