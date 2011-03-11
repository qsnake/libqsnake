#!/usr/bin/env python

from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

setup(
    name = "libqsnake",
    cmdclass = {'build_ext': build_ext},
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
    ext_modules = [Extension("qsnake.cmesh", ["qsnake/cmesh.pyx"])],
    description = "Qsnake standard library",
    license = "BSD",
)
