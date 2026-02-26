# py-richdem

**py-richdem** provides high-performance terrain analysis and hydrologic processing
for digital elevation models (DEMs), built on the original
[**RichDEM**](https://github.com/r-barnes/richdem) C++ core
and distributed as a modern Python package with multi-platform wheels.

## Relationship with RichDEM

**py-richdem** is derived from the original **RichDEM** project by
[Richard Barnes](https://github.com/r-barnes/).

> This project does not claim authorship of upstream **RichDEM** algorithms.

This project:

* Vendors the **RichDEM** C++ terrain analysis core
* Removes components unrelated to the Python interface
* Modernizes the build and packaging system
* Provides multi-platform wheels
* Maintains a focused Python distribution

This project does **not** aim to:

* Replace the upstream C++ project
* Redesign core terrain algorithms without clear documentation
* Diverge unnecessarily from upstream behavior

Changes in this repository are limited to:

* Build system modernization
* Packaging and distribution infrastructure
* Compatibility fixes
* Bug fixes required for supported Python versions
* Select performance or stability improvements

## Attribution and Citation

All scientific credit for the terrain analysis algorithms belongs to the original
authors of **RichDEM**.

If you use this software in academic work, please cite:

* The original RichDEM publication(s)
* This repository (if appropriate for reproducibility)
