import sys
import warnings

from richdem import _richdem as _rd

sys.modules[__name__] = _rd

warnings.warn(
    "The `_richdem` module is now inside the `richdem` package and"
    " is considered a private API. Direct imports will be removed in v3.0."
    " Use the public functions from `richdem` instead.",
    DeprecationWarning,
    stacklevel=2,
)
