import os
import sys

from pybind11.setup_helpers import Pybind11Extension
from setuptools import setup

is_windows = sys.platform.startswith("win")
is_macos = sys.platform == "darwin"
is_linux = sys.platform.startswith("linux")

richdem_prefix = os.environ.get("RICHDEM_PREFIX")
openmp_prefix = os.environ.get("OPENMP_PREFIX")

sources: list[str] = ["cpp/pywrapper.cpp"]

include_dirs: list[str] = []
library_dirs: list[str] = []
extra_objects: list[str] = []
libraries: list[str] = []
extra_link_args: list[str] = []
extra_compile_args: list[str] = []
define_macros: list[str, str | None] = []

if richdem_prefix:
    include_dirs.append(os.path.join(richdem_prefix, "include"))
    library_dirs.append(os.path.join(richdem_prefix, "lib"))
    if is_windows:
        libraries.append("richdem")
    else:
        extra_objects.append(os.path.join(richdem_prefix, "lib", "librichdem.a"))
else:
    if is_windows:
        libraries.append("richdem")
    else:
        extra_objects.append("librichdem.a")

if openmp_prefix:
    include_dirs.append(os.path.join(openmp_prefix, "include"))
    library_dirs.append(os.path.join(openmp_prefix, "lib"))

if is_linux:
    extra_compile_args.append("-fopenmp")
    extra_link_args.append("-fopenmp")

if is_macos:
    extra_compile_args += ["-Xpreprocessor", "-fopenmp"]
    libraries.append("omp")
    if richdem_prefix:
        extra_objects.append(os.path.join(richdem_prefix, "lib", "librichdem.a"))

if is_windows:
    define_macros.append(("_USE_MATH_DEFINES", None))
    extra_compile_args = ["/O2"]


ext_modules = [
    Pybind11Extension(
        "richdem._richdem",
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
