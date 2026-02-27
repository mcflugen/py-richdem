# Changelog for py-richdem

## 2.2.0 (unreleased)

### Features

* Added a step to the CI to build wheels, using *cibuildwheel*,
  that bundle the *richdem* library. Wheels are built for
  *Linux*, *Mac*, and *Windows* and for Python 3.11+.
  * [#6](https://github.com/mcflugen/py-richdem/issues/6),
    [#9](https://github.com/mcflugen/py-richdem/issues/9),
    [#11](https://github.com/mcflugen/py-richdem/issues/11),
    [#15](https://github.com/mcflugen/py-richdem/issues/15)
* Added a publish job to the CI that will publish built
  either to PyPI or TestPyPI.
  * [#21](https://github.com/mcflugen/py-richdem/issues/21)

### Updating

* Moved the *py-richdem* package to a src-layout.
  * [#1](https://github.com/mcflugen/py-richdem/issues/1)
* Moved static metadata from *setup.py* into *pyproject.toml*.
  * [#3](https://github.com/mcflugen/py-richdem/issues/3)
* Vendored upstream *richdem* as a submodule of *py-richdem*.
  * [#4](https://github.com/mcflugen/py-richdem/issues/4),
    [#14](https://github.com/mcflugen/py-richdem/issues/14)
* Cleaned up the versioning of *py-richdem* and *richdem*.
  * [#5](https://github.com/mcflugen/py-richdem/issues/5)
* Updated the README to reflect what *py-richdem* is,
  and to give credit to [@r-barnes](https://github.com/r-barnes)
  and the upstream repository.
  * [#10](https://github.com/mcflugen/py-richdem/issues/10)
* Switched public functions from camel-case to the more standard
  snake-case.
  * [#12](https://github.com/mcflugen/py-richdem/issues/12),
    [#18](https://github.com/mcflugen/py-richdem/issues/18)
* Reorganized the *py-richdem* package:
  moved api functions from ``__init__.py`` into ``_api.py``,
  moved *gdal*-requiring functions into ``_gdal.py``,
  moved *_richdem.py* extension module inside the *richdem* package.
  * [#13](https://github.com/mcflugen/py-richdem/issues/13),
    [#16](https://github.com/mcflugen/py-richdem/issues/16),
    [#19](https://github.com/mcflugen/py-richdem/issues/19)
* Use ``isinstance`` and raise ``TypeError`` when type checking.
  * [#17](https://github.com/mcflugen/py-richdem/issues/17)
