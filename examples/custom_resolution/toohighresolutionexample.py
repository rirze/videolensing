from vidlens import VideoLens

res = VideoLens(height=10800, width=10380, lensinfo=['../sie_lens/1280x720-SIE2.0.npy'])
res.run()

"this example is intended to show that the program works even if you specify too high of a resolution"
