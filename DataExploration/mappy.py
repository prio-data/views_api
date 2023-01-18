# Mapper
import geopandas as gpd
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import contextily as ctx
import sqlalchemy as sa
#from ingester3.config import source_db_path
#from ingester3.Country import Country
#from ingester3.extensions import *
#from ingester3.ViewsMonth import ViewsMonth

from views_dataviz.map import mapper, utils
from views_dataviz import color
from views_dataviz.map.presets import ViewsMap
from views_dataviz.map import utils
from matplotlib import pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

class Mapper2:
    """
    `Map` takes basic properties and allows the user to consecutively add
    layers to the Map object. This makes it possible to prepare mapping
    "presets" at any level of layeredness that can be built on further.
    
    Mapper2 allows for the customizable addition of scaling to the map. 
    -re-add the code for labels later when i can test it

    Attributes
    ----------
    width: Integer value for width in inches.
    height: Integer value for height in inches.
    bbox: List for the bbox per [xmin, xmax, ymin, ymax].
    frame_on: Bool for whether to draw a frame around the map.
    title: Optional default title at matplotlib's default size.
    figure: Optional tuple of (fig, size) to use if you want to plot into an
        already existing fig and ax, rather than making a new one.
    """

    def __init__(
        self,
        width,
        height,
        bbox=None,
        cmap=None,
        frame_on=True,
        title="",  # Default title without customization. (?)
        figure=None,
    ):
        self.width = width
        self.height = height
        self.bbox = bbox  # xmin, xmax, ymin, ymax
        self.cmap = cmap
        if figure is None:
            self.fig, self.ax = plt.subplots(figsize=(self.width, self.height))
        else:
            self.fig, self.ax = figure
        self.texts = []
        self.ax.set_title(title)

        if frame_on:  # Remove axis ticks only.
            self.ax.tick_params(
                top=False,
                bottom=False,
                left=False,
                right=False,
                labelleft=False,
                labelbottom=False,
            )
        else:
            self.ax.axis("off")

        if bbox is not None:
            self.ax.set_xlim((self.bbox[0], self.bbox[1]))
            self.ax.set_ylim((self.bbox[2], self.bbox[3]))

    def add_layer(self, gdf, map_scale=False, map_dictionary=False, cmap=None, inform_colorbar=False, **kwargs):
        """Add a geopandas plot to a new layer.

        Parameters
        ----------
        gdf: Geopandas GeoDataFrame to plot.
        cmap: Optional matplotlib colormap object or string reference
            (e.g. "viridis").
        inform_colorbar: Set or overwrite colorbar with the current layer.
            Not applicable when `color` is supplied in the kwargs.
        map_scale: set a manual scale for the map. If missing defaults to the Remco procedure. 
        map_dictionary: set manual labels for the map. If missing defaults to the default labels.
        **kwargs: Geopandas `.plot` keyword arguments.
        """
        if "color" in kwargs:
            colormap = None
        else:
            colormap = self.cmap if cmap is None else cmap
            if inform_colorbar and "column" in kwargs:
                if hasattr(self, "cax"):
                    self.cax.remove()
                if "vmin" not in kwargs:
                    self.vmin = gdf[kwargs["column"]].min()
                else:
                    self.vmin = kwargs["vmin"]
                if "vmax" not in kwargs:
                    self.vmax = gdf[kwargs["column"]].max()
                else:
                    self.vmax = kwargs["vmax"]
        
        try: Mapper2.add_colorbar(self, colormap, min(map_scale), max(map_scale))
        except: Mapper2.add_colorbar(self, colormap, self.vmin, self.vmax)
        
        try:
            self.ax = gdf.plot(ax=self.ax, cmap=colormap, vmin=min(map_scale), vmax=max(map_scale), **kwargs)
        except: 
            self.ax = gdf.plot(ax=self.ax, cmap=colormap, **kwargs)

                
        return self
    
    def add_colorbar(
        self,
        cmap,
        vmin,
        vmax,
        location="right",
        size="5%",
        pad=0.1,
        alpha=1,
        labelsize=16,
        tickparams=None,
    ):
        """Add custom colorbar to Map.

        Needed since GeoPandas legend and plot axes do not align, see:
        https://geopandas.readthedocs.io/en/latest/docs/user_guide/mapping.html

        Parameters
        ----------
        cmap: Matplotlib colormap object or string reference (e.g. "viridis").
        vmin: Minimum value of range colorbar.
        vmax: Maximum value of range colorbar.
        location: String for location of colorbar: "top", "bottom", "left"
            or "right".
        size: Size in either string percentage or number of pixels.
        pad: Float for padding between the plot's frame and colorbar.
        alpha: Float for alpha to apply to colorbar.
        labelsize: Integer value for the text size of the ticklabels.
        tickparams: Dictionary containing value-label pairs. For example:
            {0.05: "5%", 0.1: "10%"}
        """
        norm = plt.Normalize(vmin, vmax)
        if isinstance(cmap, str):
            cmap = plt.get_cmap(cmap)
        cmap = color.force_alpha_colormap(cmap=cmap, alpha=alpha)
        scalar_to_rgba = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
        divider = make_axes_locatable(self.ax)
        self.cax = divider.append_axes(location, size, pad)
        self.cax.tick_params(labelsize=labelsize)
        tickvalues = (
            list(tickparams.keys()) if tickparams is not None else None
        )
        self.cbar = plt.colorbar(
            scalar_to_rgba, cax=self.cax, ticks=tickvalues
        )
        if tickparams is not None:
            self.cbar.set_ticklabels(list(tickparams.values()))
        return self
    
    def save(
        self, path, dpi=200, **kwargs
    ):  # Just some defaults to reduce work.
        """Save Map figure to file.
        Parameters
        ----------
        path: String path, e.g. "./example.png".
        dpi: Integer dots per inch. Increase for higher resolution figures.
        **kwargs: Matplotlib `savefig` keyword arguments.
        """
        self.fig.savefig(path, dpi=dpi, bbox_inches="tight", **kwargs)
        plt.close(self.fig)
        

def vid2date(i):
    year=str(1980 + i//12)
    month=str(i%12)
    return year+'/'+month

#note the zip function occured earlier
# standard_scale = [np.log1p(0),np.log1p(3),np.log1p(10), np.log1p(30), np.log1p(100),  np.log1p(300)]#, np.log1p(1000), np.log1p(3000),  np.log1p(10000)]

# standard_scale_labels = ['0', '3','10', '30','100', '300']#, '1000', '3000', '10000']

# small_scale=[np.log1p(0),np.log1p(3),np.log1p(10), np.log1p(30), np.log1p(100),  np.log1p(300)]#, np.log1p(1000)]


# small_scale_labels = ['0', '3','10', '30','100', '300']#, '1000']

# small_scale_nolabels = ['', '','', '','', '', '']