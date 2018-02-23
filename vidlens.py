import numpy as np
import cv2
from scipy import misc
from scipy.interpolate import griddata as sgriddata
import sys
import collections as coll
import warnings


class VideoLens:

    def __init__(self, width=None, height=None, pixelscale=0.01,
                 lensinfo=None, show_unlensed=True, draw_caustics=False, ui='cv'):

        self.set_dims(width, height)

        self.pixelscale = pixelscale
        self.show_unlensed = show_unlensed
        self.draw_caustics = draw_caustics
        self.ui = ui
        if ui not in self.list_uis():
            raise ValueError("Specified ui parameter is not recognized: " +
                             ui + "\nMust be one of the following: " + str(self.list_uis()))

        self.process_lensinfo(lensinfo)

    def list_uis(self):
        return ['cv', 'qt', 'pg']

    def setup_camera(self):
        self.vid_cap = cv2.VideoCapture(0)

    def set_dims(self, width, height):
        self.setup_camera()

        very_high_resolution = 100000

        # here, we set the video capture to highest resolution
        # it is difficult to generically figure out the capture resolutions of any webcam,
        # so rather we use the maxiumum size or crop out to the size specified
        self.vid_cap.set(3, very_high_resolution)
        self.vid_cap.set(4, very_high_resolution)

        val, frame = self.vid_cap.read()
        if not val:
            raise RuntimeError("Camera failed to take image.")

        vid_height, vid_width = frame.shape[0:2]
        self.vid_height = vid_height
        self.vid_width  = vid_width
        # if the given dimensions are higher than what the webcam can capture,
        # ignore them and go with the highest it can capture.
        # otherwise stick with given dimensions (that are obviously smaller than max)
        self.height = height if height and vid_height>height else vid_height
        self.width  = width  if width  and vid_width >width  else vid_width

    def get_1D_coords(self, arr, dims=None):
        if dims is None:
            dims = (self.height, self.width)
        return np.ravel_multi_index(np.array(arr), dims).reshape(dims)

    def get_2D_coords(self, arr, dims=None):
        if dims is None:
            dims = (self.height, self.width)
        return np.unravel_index(np.array(arr.ravel()), dims)
    
    def crop(self, arr, mapping=False):
        img_height, img_width = arr.shape[0:2]
        if img_height < self.height or img_width < self.width:
            raise ValueError(
                "Interpolation given is not large enough for video frame dimensions: " +
                "mapping is of dimensions " + str(img_height) + ", " + str(img_width) +
                ", while video is capturing at " + str(self.height) + ", " + str(self.width))

        dif_height = (img_height - self.height) / 2
        dif_width = (img_width - self.width) / 2

        
        if dif_height == 0 and dif_width == 0:
            return arr
        elif dif_height == 0:
            newarr = arr[:, dif_width:-dif_width]
        elif dif_width == 0:
            newarr = arr[dif_height:-dif_height, :]
        else:
            newarr = arr[dif_height:-dif_height, dif_width:-dif_width]

        if mapping:
            newarr[:,:,0] -= dif_height
            newarr[:,:,1] -= dif_width

        return newarr
            

    def process_lensinfo(self, lensinfo):

        if bool(lensinfo) is False:  # check for None and []
            raise ValueError("No information given about lens(es)")

        def open_and_load_file(filename):
            if filename.endswith('.npy'):
                return np.load(filename)
            elif filename.endswith('.png'):
                # cv2 reads in floats...
                img = misc.imread(filename).astype('int')
                # this formula was used by Towes, so we'll just adopt here as
                # well
                return 100 * img[:, :, 1] + img[:, :, 0]
            else:
                raise ValueError(
                    "Don't know how to open this file: " + filename)

        # information is given in file(s)
        if isinstance(lensinfo, coll.Iterable) and isinstance(
                lensinfo[0], str):
            if len(lensinfo) == 1:
                temp_totind = self.crop(open_and_load_file(lensinfo[0]), mapping=True)
                # shape: (height, width, 2) -^
                v_and_u = temp_totind.transpose([2, 0, 1])
                # shape (2, height, width) -^
                
                self.totind = self.get_1D_coords(v_and_u)

            elif len(lensinfo) == 2:
                self.uind = self.crop(open_and_load_file(lensinfo[0]))
                self.vind = self.crop(open_and_load_file(lensinfo[1]))

                self.totind = self.get_1D_coords((self.vind, self.uind))

        # calculate info from gravlens
        # recognizing class is not really elegant...
        elif lensinfo.__class__.__name__ is 'gravlens':
            if not hasattr(lensinfo, 'u'):
                lensinfo.generate_ranges()
                lensinfo.transformations()

            self.x, self.y = lensinfo.grid.T
            self.u, self.v = lensinfo.transformed.T
            if self.draw_caustics:
                self.caustics = lensinfo.caustics
            self.interpolate()

        else:
            raise ValueError(
                "Don't know how to interpret this lensinfo:" +
                str(lensinfo))

    def interpolate(self):
        # the real meat of this process
        
        ximin = -self.width / 2.0 + 1.0
        ximax = self.width / 2.0
        yimin = -self.height / 2.0 + 1.0
        yimax = self.height / 2.0

        xi = np.linspace(ximin, ximax, self.width)
        yi = np.linspace(yimin, yimax, self.height)

        # we convert the image and source positions to pixels
        xp = self.x / self.pixelscale
        yp = self.y / self.pixelscale
        up = self.u / self.pixelscale
        vp = self.v / self.pixelscale

        # and interpolate :
        points = np.transpose((xp, yp))
        # cartesian product of xi & yi
        grid = np.dstack(np.meshgrid(xi, yi)).reshape(-1, 2)
        ui = sgriddata(points, up, grid, method='cubic', fill_value=0)
        vi = sgriddata(points, vp, grid, method='cubic', fill_value=0)

        # and shift the origin to the lower left corner :
        uis = ui - ximin
        vis = vi - yimin

        # We round to the nearest int (all this should be positive now) :
        self.uind = (np.around(uis)).astype('int')
        self.vind = (np.around(vis)).astype('int')

        # since the image that will be 'lensed' is a 1D array, turn 2D coords into 1D coords
        # self.totind = self.uind*self.width + self.uind
        self.totind = self.get_1D_coords((self.vind, self.uind))

        # setup critical/caustics onto grid
        if self.draw_caustics:
            self.caustics = np.array(self.caustics) / self.pixelscale
            [self.critx, self.crity], [self.caustx, self.causty] = self.caustics
            self.critx  = self.critx.astype('int')  + self.width  / 2
            self.crity  = self.crity.astype('int')  + self.height / 2
            self.caustx = self.caustx.astype('int') + self.width  / 2
            self.causty = self.causty.astype('int') + self.height / 2

    # @profile
    def lensing_routine(self, image_format='rgb'):

        # Capture frame-by-frame
        ret, frame = self.vid_cap.read()
        frame = self.crop(frame)

        # for some reason, image flips left-right
        self.unlensed = np.fliplr(frame)

        # quicker than:
        # lensedimg = frame[self.uind, self.vind]
        np.take(self.unlensed.reshape((-1, 3)),
                self.totind, axis=0, out=self.lensedimg)

        # draw critical lines and caustics
        if self.draw_caustics:
            # remember, colors are in bgr format! (thanks opencv...)
            self.lensedimg[self.crity, self.critx] = [0, 0, 255]  # red
            self.unlensed[self.causty, self.caustx] = [255, 0, 0]  # green

        if image_format is 'bgr':
            return
        elif image_format is 'rgb':
            self.unlensed = self.unlensed[:, :, ::-1]
            self.lensedimg = self.lensedimg[:, :, ::-1]
        else:
            raise ValueError(
                "Image Format: " +
                image_format +
                " Not Supported!")

    def lens_start(self):

        if self.show_unlensed:
            cv2.namedWindow('original')
        cv2.namedWindow('lensed')

        # infinite loop until one presses 'q'
        while(not (cv2.waitKey(1) & 0xFF == ord('q'))):

            self.lensing_routine(image_format='bgr')

            # Display the resulting image
            if self.show_unlensed:
                cv2.imshow('original', self.unlensed)
            cv2.imshow('lensed', self.lensedimg)

        # cv2.destroyWindow('frame') # causes a weird python freeze, just close it out manually
        # cv2.destroyAllWindows()

    def save_interpolation(self, file_names, extension=None):
        if isinstance(file_names, str):
            file_names = [file_names]

        if extension is not None:
            full_file_names = [name + '.' + extension for name in file_names]
        else:
            full_file_names = file_names

        # TODO: Implement flexible saving mechanism, define custom save
        # function based on file extension
        if extension == 'npy':
            if len(full_file_names) == 1:
                temp_totind = np.array(self.get_2D_coords(self.totind))
                temp_totind = temp_totind.reshape(
                    (2, self.height, self.width)).transpose([1, 2, 0])
                np.save(full_file_names[0], temp_totind)
            elif len(full_file_names) == 2:
                np.save(full_file_names[0], self.get_2D_coords(self.xind))
                np.save(full_file_names[1], self.get_2D_coords(self.yind))
            else:
                raise ValueError(
                    "Too many files to save, should be given one or two files")
        else:
            raise ValueError(
                "Do not know how to save interpolation as ." +
                extension)

    def release_camera(self):
        self.vid_cap.release()

    def run(self):
        dims = (self.height, self.width, 3)
        self.unlensed = np.empty(dims, dtype='uint8')
        self.lensedimg = np.empty(dims, dtype='uint8')

        if self.ui is 'cv':
            self.lens_start()
        elif self.ui is 'qt':
            import qtgui
            qtgui.lens_start(self)
        elif self.ui is 'pg':
            import pyqtgraphgui as pgg
            pgg.lens_start(self)
            
        # When everything done, release the capture
        self.vid_cap.release()

        sys.exit(0)
