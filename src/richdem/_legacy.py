import functools
import warnings

from richdem._api import _add_analysis
from richdem._api import _format_richdem_version
from richdem._api import breach_depressions
from richdem._api import fill_depressions
from richdem._api import flow_accum_from_props
from richdem._api import flow_accumulation
from richdem._api import flow_proportions
from richdem._api import load_gdal
from richdem._api import rd_show
from richdem._api import resolve_flats
from richdem._api import save_gdal
from richdem._api import terrain_attribute


def _deprecated_alias(new_func, old_name, *, removal_version="TBD"):
    @functools.wraps(new_func)
    def wrapper(*args, **kwargs):
        warnings.warn(
            f"{old_name} is deprecated; use {new_func.__name__} instead. "
            f"Planned removal in v{removal_version}.",
            DeprecationWarning,
            stacklevel=2,
        )
        return new_func(*args, **kwargs)

    wrapper.__doc__ = f"DEPRECATED: Use `{new_func.__name__}` instead.\n\n" + (
        new_func.__doc__ or ""
    )
    wrapper.__name__ = old_name
    wrapper.__qualname__ = old_name
    return wrapper


_RichDEMVersion = _deprecated_alias(_format_richdem_version, "_RichDEMVersion")
_AddAnalysis = _deprecated_alias(_add_analysis, "_AddAnalysis")
rdShow = _deprecated_alias(rd_show, "rdShow")
LoadGDAL = _deprecated_alias(load_gdal, "LoadGDAL")
SaveGDAL = _deprecated_alias(save_gdal, "SaveGDAL")
FillDepressions = _deprecated_alias(fill_depressions, "FillDepressions")
BreachDepressions = _deprecated_alias(breach_depressions, "BreachDepressions")
ResolveFlats = _deprecated_alias(resolve_flats, "ResolveFlats")
FlowAccumulation = _deprecated_alias(flow_accumulation, "FlowAccumulation")
FlowAccumFromProps = _deprecated_alias(flow_accum_from_props, "FlowAccumFromProps")
FlowProportions = _deprecated_alias(flow_proportions, "FlowProportions")
TerrainAttribute = _deprecated_alias(terrain_attribute, "TerrainAttribute")
