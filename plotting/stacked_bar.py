import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def stacked_bar(df, x, y, stacks = None, color_dict = None, x_order = None):
    '''
    Wrapper to make a seaborn stacked bar plot

    df - dataframe where columns are data categories
    x - data category (df column) for the x axis 
    y - data category (df column) for the stacks
    stacks - data category (df column) of stack proportions if values == "prop"
    colors - optional parameter for customizing colors format: [(value: color), (value: color),...]

    '''
    if stacks == None:
        bp_df = df.loc[:, [x, y]] 
    else:
        bp_df = df.loc[:, [x, y, stacks]]
        bp_df[stacks] = round(bp_df[stacks]*100)

    all_xs = set(bp_df[x].values)
    for an, color in color_dict:
        print(an)
        if stacks == None:
            total_bp_df = bp_df[x].value_counts().reset_index().sort_values("count")
        else:
            total_bp_df = bp_df.loc[:, [x, stacks]]
            total_bp_df.columns = [x, "count"]

        xs = set(total_bp_df[x].values)
        xs_diff = all_xs.difference(xs)
        if len(xs_diff) !=0:
            add_df = pd.DataFrame(index = range(len(xs_diff)), data = np.transpose([list(xs_diff), [0]*len(xs_diff)]), columns = [x, "count"]) 
            total_bp_df = pd.concat([total_bp_df, add_df])
            total_bp_df["count"] = total_bp_df["count"].astype(int)
            total_bp_df.sort_values("count")

        if stacks != None:
            total_bp_df = total_bp_df.groupby("count").sum().reset_index()

        sns.barplot(y = "count", x = x, data = total_bp_df, color = color, order = x_order, orient = "v", errorbar = None)

        bp_df = bp_df.loc[bp_df[y]!=an]
    plt.show() 
