#!/usr/bin/env python

from numpy.distutils.core import setup
from numpy.distutils.extension import Extension
from numpy.distutils.command.build_ext import build_ext as numpy_build_ext
from Cython.Distutils import build_ext as cython_build_ext
import numpy

class build_ext(numpy_build_ext, cython_build_ext):
    pass

setup(
    name = "libqsnake",
#    cmdclass = {'build_ext': build_ext},
    version = "0.1",
    packages = [
        'qsnake',
        'qsnake.calculators',
        'qsnake.calculators.tests',
        'qsnake.data',
        'qsnake.mesh2d',
        'qsnake.tests',
        ],
    package_data = {
        'qsnake.tests': ['phaml_data/domain.*'],
        },
    include_dirs=[numpy.get_include()],
    #    ext_modules = [Extension("qsnake.cmesh", [
    #    "qsnake/cmesh.pyx",
    #    #"qsnake/fmesh.f90",
    #    ])],
    description = "Qsnake standard library",
    license = "BSD",
)
