import os
import sys

from pybind11.setup_helpers import Pybind11Extension
from setuptools import setup

richdem_prefix = os.environ.get("RICHDEM_PREFIX")
openmp_prefix = os.environ.get("OPENMP_PREFIX")

sources: list[str] = ["cpp/pywrapper.cpp"]

include_dirs: list[str] = []
library_dirs: list[str] = []
extra_objects: list[str] = []
libraries: list[str] = []
extra_link_args: list[str] = []
extra_compile_args: list[str] = ["-fvisibility=hidden", "-O3"]
define_macros: list[str, str | None] = [("DOCTEST_CONFIG_DISABLE", None)]

if richdem_prefix:
    include_dirs.append(os.path.join(richdem_prefix, "include"))
    library_dirs.append(os.path.join(richdem_prefix, "lib"))
    extra_objects.append(os.path.join(richdem_prefix, "lib", "librichdem.a"))
else:
    extra_objects.append("librichdem.a")

if openmp_prefix:
    include_dirs.append(os.path.join(openmp_prefix, "include"))
    library_dirs.append(os.path.join(openmp_prefix, "lib"))

    if sys.platform == "darwin":
        extra_compile_args += ["-Xpreprocessor", "-fopenmp"]
        libraries.append("omp")

if sys.platform == "linux":
    extra_compile_args.append("-fopenmp")
    extra_link_args.append("-fopenmp")

if sys.platform.startswith("win"):
    define_macros.append(("_USE_MATH_DEFINES", None))

ext_modules = [
    Pybind11Extension(
        "_richdem",
        sources,
        include_dirs=include_dirs,
        library_dirs=library_dirs,
        libraries=libraries,
        extra_compile_args=extra_compile_args,
        extra_link_args=extra_link_args,
        extra_objects=extra_objects,
        cxx_std=17,
        define_macros=define_macros,
    ),
]


setup(ext_modules=ext_modules)
