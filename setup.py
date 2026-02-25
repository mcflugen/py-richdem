import glob
import re
import setuptools
import subprocess
from setuptools.command.build_ext import build_ext as _build_ext
from setuptools import setup
from typing import Optional

from pybind11.setup_helpers import Pybind11Extension

richdem_compile_time: Optional[str] = None
richdem_git_hash: Optional[str]     = None

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

if richdem_git_hash is None:
  try:
    shash = subprocess.Popen(["git log --pretty=format:'%h' -n 1"], shell=True, stderr=subprocess.STDOUT, stdout=subprocess.PIPE).stdout.readlines()[0].decode('utf8').strip()
    sdate = subprocess.Popen(["git log -1 --pretty='%ci'"], shell=True, stderr=subprocess.STDOUT, stdout=subprocess.PIPE).stdout.readlines()[0].decode('utf8').strip()
    if re.match(r'^[0-9a-z]+$', shash) and re.match(r'^[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}.*$', sdate):
      richdem_compile_time = sdate
      richdem_git_hash     = shash
  except:
    print("Warning! Could not find RichDEM version. Software will still work, but reproducibility will be compromised.")
    pass

if richdem_git_hash is None:
  richdem_compile_time = 'Unknown'
  richdem_git_hash     = 'Unknown'

print("Using RichDEM hash={0}, time={1}".format(richdem_git_hash, richdem_compile_time))

ext_modules = [
    Pybind11Extension(
      "_richdem",
      sorted(glob.glob('src/*.cpp') + glob.glob('lib/richdem/src/**/*.cpp', recursive=True)),
      include_dirs  = ['lib/richdem/include/'],
      define_macros = [
        ('DOCTEST_CONFIG_DISABLE', None),
        ('RICHDEM_COMPILE_TIME',   f'"\\"{richdem_compile_time}\\""'),
        ('RICHDEM_GIT_HASH',       f'"\\"{richdem_git_hash}\\""'    ),
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
