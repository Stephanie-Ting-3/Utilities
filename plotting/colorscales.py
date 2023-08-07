'''
Functions to handle mapping values to colors for seaborn clustermap

Author: Stephanie Ting
Stephanie.Ting.3@gmail.com
7/24/2023

Last edited:
8/4/2023
'''

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
    Internal function that maps continuous variable to 
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
    '''
    Internal function that maps a categorical or binary variable to 
    sns color palettes.

    s - pandas Series to be mapped
    values - values in pandas Series
    dtype - 'categorical' or 'binary' - determines what color 
                            color palette will be used

    Returns pandas Series object
    '''
    
    if dtype == 'categorical':
        colorscheme = sns.color_palette("bright")+sns.color_palette("pastel")
    elif dtype == 'binary':
        colorscheme = [black, gray, white]

    color_dict=dict(zip(values, colorscheme))
    

    #Return color key as well for referencing
    return((s.map(color_dict), color_dict))

def make_color_annotations(ds, datatype, normalization_method = "linear", color_value_order = None):

    '''
    Makes a color annotation pandas Series or DataFrame mapping value to rgba value 
    (intended for seaborn.clustermap)

    ds - pandas DataFrame object with each category of features to be mapped as
        columns and the features as rows

    datatype - iterable containing "continuous", "categorical", and/or "binary"
    color_value_order - dict of lists of values for order in which values should be assigned to colors. 
                        if None, values will be sorted ascending numerically or alphabetically
                        
                        for categorical colors the colors are in order of palette "bright"
                        followed by "pastel"
                        
                        for binary colors the colors are in order of black, gray, white 
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
    return_keys=[]

    for column, dtype in zip(ds.columns, datatype):
        group=ds.loc[:, column]

        if not dtype in ["continuous", "categorical", "binary"]:
            raise AssertionError(
                    "datatype must be \"continuous\", \"categorical\", or \"binary\""
                    )
               
        if dtype == "continuous":
            group=group.astype(float)
            if normalization_method == "linear":
                return_series.append(_mpl_normalize(group, matplotlib.colors.Normalize,
                                                    vmin=group.quantile(0.25),
                                                    vmax=group.quantile(0.75))[0])
                return_keys.append(None)

            elif normalization_method == "centered":
                return_series.append(_mpl_normalize(group, matplotlib.colors.CenteredNorm,
                                                    vcenter = np.median(group.values)
                                                    )[0])
                return_keys.append(None)
            else:
                raise AssertionError(
                        "method must be \"linear\" or \"centered\""

            )             
        else:
            #This is to control the order that values are assigned to colors
            #If an order is preferred
            if color_value_order == None:
                value_order = list(set(group.values))
                value_order.sort()

            elif column in color_value_order:
                if type(color_value_order[column]) == list and  len(color_value_order[column]) == len(set(group.values)):
                    value_order = color_value_order[column]
                else:
                    raise AssertionError(
                            "color_value_order must be a dict with column names as keys and list of values to map as values"
                            )
                    
            cat_colors = _map_categorical_colors(group, value_order, dtype)
            return_series.append(cat_colors[0])
            return_keys.append(cat_colors[1])
    
    return((pd.DataFrame(return_series), return_keys))
        
        

