import glob
import re
import setuptools
import subprocess
from setuptools.command.build_ext import build_ext as _build_ext
from setuptools import setup
from typing import Optional

from pybind11.setup_helpers import Pybind11Extension


#Compiler specific arguments
BUILD_ARGS = {
  'msvc': ['-std=c++11','-g','-fvisibility=hidden','-O3'],
  'gcc':  ['-std=c++11','-g','-fvisibility=hidden','-O3','-Wno-unknown-pragmas'],
  'unix': ['-std=c++11','-g','-fvisibility=hidden','-O3','-Wno-unknown-pragmas']
}

#Magic that hooks compiler specific arguments up with the compiler
class build_ext_compiler_check(_build_ext):
  def build_extensions(self):
    compiler = self.compiler.compiler_type
    print(f'COMPILER {compiler}')
    args     = BUILD_ARGS[compiler]
    for ext in self.extensions:
        ext.extra_compile_args = args
        print(f'COMPILER ARGUMENTS: {ext.extra_compile_args}')
    _build_ext.build_extensions(self)

ext_modules = [
    Pybind11Extension(
      "_richdem",
      sorted(glob.glob('src/*.cpp') + glob.glob('lib/richdem/src/**/*.cpp', recursive=True)),
      include_dirs  = ['lib/richdem/include/'],
      define_macros = [
        ('DOCTEST_CONFIG_DISABLE', None),
        ('RICHDEM_LOGGING',        None),
        ('_USE_MATH_DEFINES',      None) #To ensure that `#include <cmath>` imports `M_PI` in MSVC
      ]
    ),
]

long_description = """RichDEM is a set of digital elevation model (DEM) hydrologic analysis tools.

RichDEM uses parallel processing and state of the art algorithms to quickly process even very large DEMs.

RichDEM offers a variety of flow metrics, such as D8 and D-infinity.

It can flood or breach depressions, as well as calculate flow accumulation, slopes, curvatures, &c."""


#TODO: https://packaging.python.org/tutorials/distributing-packages/#configuring-your-project
setup(
    ext_modules=ext_modules,
    cmdclass={"build_ext": build_ext_compiler_check},
)
