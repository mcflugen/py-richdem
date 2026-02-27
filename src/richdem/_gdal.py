import numpy as np

from richdem._api import _add_analysis
from richdem._api import rdarray


def _require_gdal():
    try:
        from osgeo import gdal
    except ModuleNotFoundError as error:
        raise ModuleNotFoundError(
            "GDAL support is not installed. Install with 'pip install gdal'"
            " or via conda-forge."
        ) from error
    return gdal


def load_gdal(filename, no_data=None):
    """Read a GDAL file.

    Opens any file GDAL can read, selects the first raster band, and loads it
    and its metadata into a RichDEM array of the appropriate data type.

    If you need to do something more complicated, look at the source of this
    function.

    Args:
        filename (str):    Name of the raster file to open
        no_data  (float):  Optionally, set the no_data value to this.

    Returns:
        A RichDEM array
    """
    gdal = _require_gdal()

    allowed_types = {
        gdal.GDT_Byte,
        gdal.GDT_Int16,
        gdal.GDT_Int32,
        gdal.GDT_UInt16,
        gdal.GDT_UInt32,
        gdal.GDT_Float32,
        gdal.GDT_Float64,
    }

    # Read in data
    src_ds = gdal.Open(filename)
    srcband = src_ds.GetRasterBand(1)

    if no_data is None:
        no_data = srcband.GetNoDataValue()
        if no_data is None:
            raise Exception(
                "The source data did not have a NoData value. Please use the no_data"
                " argument to specify one. If should not be equal to any of the"
                " actual data values. If you are using all possible data values,"
                " then the situation is pretty hopeless - sorry."
            )

    srcdata = rdarray(srcband.ReadAsArray(), no_data=no_data)

    # raster_srs = osr.SpatialReference()
    # raster_srs.ImportFromWkt(raster.GetProjectionRef())

    if srcband.DataType not in allowed_types:
        raise Exception(
            "This datatype is not supported. Please file a bug report on RichDEM."
        )

    srcdata.projection = src_ds.GetProjectionRef()
    srcdata.geotransform = src_ds.GetGeoTransform()

    srcdata.metadata = {}
    for k, v in src_ds.GetMetadata().items():
        srcdata.metadata[k] = v

    _add_analysis(srcdata, f"load_gdal(filename={filename}, no_data={no_data})")

    return srcdata


def save_gdal(filename, rda):
    """Save a GDAL file.

    Saves a RichDEM array to a data file in GeoTIFF format.

    If you need to do something more complicated, look at the source of this
    function.

    Args:
        filename (str):     Name of the raster file to be created
        rda      (rdarray): Data to save.

    Returns:
        No Return
    """
    gdal = _require_gdal()

    if not isinstance(rda, rdarray):
        raise TypeError("A richdem.rdarray or numpy.ndarray is required!")

    driver = gdal.GetDriverByName("GTiff")
    data_type = gdal.GDT_Float32  # TODO
    data_set = driver.Create(
        filename, xsize=rda.shape[1], ysize=rda.shape[0], bands=1, eType=data_type
    )
    data_set.SetGeoTransform(rda.geotransform)
    data_set.SetProjection(rda.projection)
    band = data_set.GetRasterBand(1)
    band.SetNoDataValue(rda.no_data)
    band.WriteArray(np.array(rda))
    for k, v in rda.metadata.items():
        data_set.SetMetadataItem(str(k), str(v))
