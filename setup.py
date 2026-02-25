import glob
import os
import re
import sys
import subprocess
from setuptools.command.build_ext import build_ext as _build_ext
from setuptools import setup
from typing import Optional

from pybind11.setup_helpers import Pybind11Extension

richdem_prefix = os.environ.get("RICHDEM_PREFIX", sys.prefix)
openmp_prefix = os.environ.get("OPENMP_PREFIX", sys.prefix)

#Compiler specific arguments
BUILD_ARGS = {
  'msvc': ['-std=c++17','-g','-fvisibility=hidden','-O3'],
  'gcc':  ['-std=c++17','-g','-fvisibility=hidden','-O3'],
  'unix': ['-std=c++17','-g','-fvisibility=hidden','-O3'],
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
      ["cpp/pywrapper.cpp"],
      include_dirs = [
          os.path.join(richdem_prefix, "include"),
          os.path.join(openmp_prefix, "include"),
      ],
      library_dirs = [
          os.path.join(richdem_prefix, "lib"),
          os.path.join(openmp_prefix, "lib"),
      ],
      libraries=["omp"],
      extra_objects=[os.path.join(richdem_prefix, "lib", "librichdem.a")],
      define_macros = [
        ('DOCTEST_CONFIG_DISABLE', None),
        ('RICHDEM_LOGGING',        None),
        ('_USE_MATH_DEFINES',      None)
      ],
    ),
]

long_description = """RichDEM is a set of digital elevation model (DEM) hydrologic analysis tools.

RichDEM uses parallel processing and state of the art algorithms to quickly process even very large DEMs.

RichDEM offers a variety of flow metrics, such as D8 and D-infinity.

It can flood or breach depressions, as well as calculate flow accumulation, slopes, curvatures, &c."""


setup(
    ext_modules=ext_modules,
    cmdclass={"build_ext": build_ext_compiler_check},
)
