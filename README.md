# VideoLensing
This is a demonstration that takes the video feed from your webcam and transforms it as if it passed by a gravitational lens.

## Acknowledgments
The idea for this program is not mine, and came from a project written by [Malte Tewes](https://astro.uni-bonn.de/~mtewes/wiki/doku.php). His program, [QCgravlens](http://obswww.unige.ch/~tewes/QCgravlens/), uses a webcam on Apple computers to simulate the gravitational lensing according the lens system RXJ1131-1231.

This package is an attempt to bring the idea of his project to a more portable codebase (through the use of python and its libraries) and to expand the interface to allow users to specify their own lens maps. [`gravpy`](https://github.com/rirze/lens-solver) is needed for the second feature, and as such, I want to thank [Chuck Keeton](http://www.physics.rutgers.edu/~keeton/) for developing [`gravlens`](http://xxx.lanl.gov/abs/astro-ph/0102340) and for guiding me in writing [`gravpy`](https://github.com/rirze/lens-solver). 

## Detailed Description
This programs operates by taking a mesh-map of the source and image plane (provided by gravlens, [python version](https://github.com/rirze/lens-solver)). By using this map, `vidlens` interpolates the missing points in the grid so the transformation between the two planes can be applied to the pixels of an image. Since a video feed is simply a continuous stream of images, we can apply this interpolated transformation image by image to generate a lensed simulation from a webcam. 

## Dependencies
#### Hard Requirements
This program is meant to be cross-platform, but comes with the price of installing multiple libraries. Specifically you will need:
+ NumPy
+ SciPy
+ OpenCV

`NumPy` and `SciPy` will be installed (if not already) using `pip` during the installation process (`python setup.py install`), **but you will independently need to install [`OpenCV`](https://breakthrough.github.io/Installing-OpenCV/) (which will automatically include the python wrappers)**. Installing `OpenCV` can be either simple or complicated, depending on your machine environment. This program was tested with `OpenCV 2.4.13`, but it ought to work with `OpenCV 3.+`, since version should not matter in regards to the operations of this package.

#### Recommended
+ [gravpy](https://github.com/rirze/lens-solver): for specifying custom lens maps. If you are interested in creating your own gravitation lens system to simulate, this package is needed. Look below for how to define your own lens maps. 
+ [PyQt4](https://riverbankcomputing.com/software/pyqt/download) or [PyQt5](https://riverbankcomputing.com/software/pyqt/download5) or [PySide](http://wiki.qt.io/Category:LanguageBindings::PySide::Downloads): This user interface makes the overall package intuitively easier to work with. Using [`qtpy`](https://pypi.python.org/pypi/QtPy), `vidlens` will use one of these libraries to display the demo. If one of the three (and `qtpy`!) is not installed, then `vidlens` will use the `OpenCV` interface, which is a very minimalist version of the demo. 


## Installation
Run this from the command line, within the top-level of the package directory:
```bash
python setup.py install
```

Make sure to use proper permissions, as always, when installing python packages.

## Quickstart
If you simply want to run a sample demo, I highly suggest looking through the examples folder for some example simulations. I would recommend running these ones first:
+ `sie_lens`
+ `qt_gui_sie` (If you have a `pyqt` library installed, along with `qtpy`, which is needed for the qt interface in `vidlens`)
+ `qc_demo` (This one is a retest of Malte Tewes' program, using his input files for RXJ1131-1231)

If you have [gravpy](https://github.com/rirze/lens-solver) installed, then feel free to run the folders with `gravpy` in the directory name. 

## Ways to create a custom demonstration
There are two primary ways of starting a demo. One is to connect to [gravpy](https://github.com/rirze/lens-solver) and specify the lens and its parameters. This takes quite a bit of time because it calculates the mesh-map, interpolates the pixel-mapping and then finally applies the transformation to the image stream from the webcam. Rather, the best way to use this program is to, for each unique lens system, interface to `gravpy` once and save the interpolation file(s) onto the disk. Then, for subsequent calls, `vidlens` will use these files to skip the calculation-intensive steps and launch the simulation rather quickly.

TODO: Add sample code that illustrates this process

