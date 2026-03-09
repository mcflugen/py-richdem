# Release Notes

## 2.2.0 (unreleased)

### Added

* Continuous integration step to build wheels using *cibuildwheel* that
  bundle the *richdem* library. Wheels are built for *Linux*, *Mac*, and
  *Windows* for Python 3.11+.

  * [#6](https://github.com/mcflugen/py-richdem/issues/6),
    [#9](https://github.com/mcflugen/py-richdem/issues/9),
    [#11](https://github.com/mcflugen/py-richdem/issues/11),
    [#15](https://github.com/mcflugen/py-richdem/issues/15)

* CI publish job for releasing built wheels to *PyPI* or *TestPyPI*.

  * [#21](https://github.com/mcflugen/py-richdem/issues/21)

* Added build configuration metadata (compiler, platform, and feature flags)
  to the bundled *richdem* library and exposed it as
  `richdem.richdem_build_string`.

  * [#28](https://github.com/mcflugen/py-richdem/issues/28)

### Changed

* Public functions renamed from camelCase to snake_case to follow
  standard Python conventions.

  * [#12](https://github.com/mcflugen/py-richdem/issues/12),
    [#18](https://github.com/mcflugen/py-richdem/issues/18)

* Reorganized the package structure:

  * moved API functions from `__init__.py` to `_api.py`
  * moved GDAL-dependent functions into `_gdal.py`
  * moved the `_richdem` extension module inside the `richdem` package

  - [#13](https://github.com/mcflugen/py-richdem/issues/13),
    [#16](https://github.com/mcflugen/py-richdem/issues/16),
    [#19](https://github.com/mcflugen/py-richdem/issues/19)

* Type checks now use `isinstance` and raise `TypeError`.

  * [#17](https://github.com/mcflugen/py-richdem/issues/17)

* Moved the *py-richdem* version definition from `richdem._version`
  into `pyproject.toml`.

  * [#25](https://github.com/mcflugen/py-richdem/issues/25)

### Build

* Moved the package to a *src-layout*.

  * [#1](https://github.com/mcflugen/py-richdem/issues/1)

* Moved static metadata from *setup.py* into *pyproject.toml*.

  * [#3](https://github.com/mcflugen/py-richdem/issues/3)

* Vendored upstream *richdem* as a git submodule.

  * [#4](https://github.com/mcflugen/py-richdem/issues/4),
    [#14](https://github.com/mcflugen/py-richdem/issues/14)

* Cleaned up version reporting for both *py-richdem* and the vendored
  *richdem* library.

  * [#5](https://github.com/mcflugen/py-richdem/issues/5)

* Disabled the *richdem* progress bar during compilation by passing
  `-DRICHDEM_NO_PROGRESS` to the CMake build.

  * [#29](https://github.com/mcflugen/py-richdem/issues/29)

### Developer

* Added a `build-richdem` *nox* session to build the vendored *richdem* library.

  * [#26](https://github.com/mcflugen/py-richdem/issues/26)

* Added an `install` *nox* session that optionally builds the vendored
  *richdem* library before installing *py-richdem*.

  * [#27](https://github.com/mcflugen/py-richdem/issues/27)

### Documentation

* Updated the README to clarify the purpose of *py-richdem* and to give
  attribution to [@r-barnes](https://github.com/r-barnes) and the upstream
  repository.

  * [#10](https://github.com/mcflugen/py-richdem/issues/10)
