import pandas as pd
import numpy as np

def get_group_members(s):
    ''' 
    Parameters:
    s - pandas Series - index is group members, values are groups

    Returns:
    Python dict with groups as keys and lists of group members per group as values
    '''

    group_members = {}
    groups = list(set(s.values))
    groups.sort()

    for group in groups:
        group_members[group] = list(s.loc[s==group].index)
    return group_members
