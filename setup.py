#!/usr/bin/env python

from distutils.core import setup

setup(
    name = "libqsnake",
    version = "0.1",
    packages = [
        'qsnake',
        'qsnake.calculators',
        'qsnake.calculators.tests',
        'qsnake.data',
        'qsnake.mesh2d',
        'qsnake.tests',
        ],
    description = "Qsnake standard library",
    license = "BSD",
)
