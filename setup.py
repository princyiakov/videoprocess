from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

#with open('requirements.txt') as reqs_f:
#    requirements = reqs_f.read().splitlines()
VERSION = '0.0.1'
DESCRIPTION = 'Rectifying corrupted video file'
LONG_DESCRIPTION = 'Rectifying video which contains frames which were shuffled and some extra ' \
                   'images are added '

# Setting up
setup(
    name="videoprocess",
    version=VERSION,
    author="Princy Pappachan",
    author_email="<iamprincypappachan@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    #install_requires=requirements,
    install_requires=['opencv-python', 'numpy', 'matplotlib', 'scikit-learn', 'imageio',
                      'scikit-image', 'setuptools'],
    keywords=['python', 'video', 'stream', 'video stream', 'video rectifier'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
