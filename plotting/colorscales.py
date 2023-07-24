import matplotlib.pyplot as plt
from matplotlib.pyplot import get_cmap
from matplotlib import cm
import matplotlib.colors
import seaborn as sns
import numpy as np
import pandas as pd

black = matplotlib.colors.to_rgba("black")
gray = matplotlib.colors.to_rgba("gray")
white = matplotlib.colors.to_rgba("white")

def _mpl_normalize(s, method, cmap='vlag', **kwargs):

    '''
    Internal function that returns mapper for mapping continuous variable to 
    matplotlib colormap

    s - pandas Series to be mapped
    cmap - String name of acceptable matplotlib colormap
    method - Normalization function for normalizing data to [0,1] scale
    **kwargs - args for normalization function

    Returns pandas Series object
    '''

    # Make sure dtype is numeric
    s=s.astype(float)

    # Create mapper using desired method and colormap
    norm = method(**kwargs)
    mapper = cm.ScalarMappable(norm=norm, cmap=get_cmap(cmap))

    return((s.map(lambda x: mapper.to_rgba(x)),))

def _map_categorical_colors(s, values, dtype = 'categorical'):
    if dtype == 'categorical':
        colorscheme = sns.color_palette("bright")+sns.color_palette("pastel")
    elif dtype == 'binary':
        colorscheme = [black, gray, white]

    color_dict=dict(zip(values, colorscheme))
    

    #Return color key as well for referencing
    return((s.map(color_dict), color_dict))

def make_color_annotations(ds, datatype, normalization_method = "linear"):

    '''
    Makes a color annotation pandas Series or DataFrame mapping value to rgba value 
    (intended for seaborn.clustermap)

    ds - pandas DataFrame object with each category of features to be mapped as
        columns and the features as rows

    datatype - iterable containing "continuous", "categorical", and/or "binary"
    '''
    
    if not len(datatype) == ds.shape[1]:
        raise AssertionError(
                "Datatype should be an iterable with length equivalent to number of columns in ds"
                )
        
    if not type(ds) == pd.core.frame.DataFrame:
        raise AssertionError(
                "ds should be of type pandas DataFrame"
                )

    return_series=[]

    for column, dtype in zip(ds.columns, datatype):
        group=ds.loc[:, column]

        if not dtype in ["continuous", "categorical", "binary"]:
            raise AssertionError(
                    "datatype must be \"continuous\", \"categorical\", or \"binary\""
                    )
               
        if dtype == "continuous":
            if normalization_method == "linear":
                return_series.append(_mpl_normalize(group, matplotlib.colors.Normalize, vmin=-2.5, vmax=2.5))
            elif normalization_method == "centered":
                return_series.append(_mpl_normalize(group, matplotlib.colors.CenteredNorm,
                                                    vcenter = np.median(group.values)
                                                    ))
            else:
                raise AssertionError(
                        "method must be \"linear\" or \"centered\""

            )             
        else:
            return_series.append(_map_categorical_colors(group, set(group.values), dtype))
    
    return(return_series)
        
        

