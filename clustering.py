'''
Written by: Stephanie Ting
Created: 9/12/2024
Last Edited: 9/12/2024
'''

import pandas as pd
from scipy.cluster.hierarchy import linkage, dendrogram

def get_cluster_within_groups_order(ds, groups_dict):
    '''
    Parameters:
    ds - pandas DataFrame - dataset to be clustered with group members in column names
    groups_dict - Python dict - keys are groups, values are lists of group members
                                Can use output from data.structuring.dataframe_ops get_group_members

    '''
    #Group members must be in columns of ds
    order = []
    for group in groups_dict:
        group_ds = ds.loc[:, groups_dict[group]]

        #Calculate linkage
        l = linkage(group_ds.T, "average", metric = "correlation")

        group_order = dendrogram(l, no_plot = True)["leaves"]

        order+=list(group_ds.iloc[:, group_order].columns)

    return order
