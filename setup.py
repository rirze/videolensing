from setuptools import setup

def setup_VideoLensing():

    setup(name='vidlens',
          version='0.1',
          description='A webcam-video simulation of gravitational lensing',
          author='Sourabh Cheedella',
          author_email='cheedella.sourabh@gmail.com',
          install_requires=['numpy','scipy'],
          extras_require ={
              'gravpy': ['git+https://github.com/rirze/lens-solver.git']
              'pyqt': ['qtpy']}
    )

def test_for_python_opencv():
    try:
        import cv2
    except:
        raise ImportError("Could not find/import Python-OpenCV, make sure it's installed before running vidlens!")


if __name__ == '__main__':
    setup_VideoLensing()
    test_for_python_opencv()
