import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def stacked_bar(df, x, y, color_dict = None, x_order = None):
    '''
    Wrapper to make a seaborn stacked bar plot

    df - dataframe where columns are data categories
    x - data category (df column) for the x axis 
    y - data category (df column) for the stacks
    colors - optional parameter for customizing colors format: [(value: color), (value: color),...]

    '''
    bp_df = df.loc[:, [x, y]]

    all_xs = set(bp_df[x].values)
    for an, color in color_dict:
        print(an)
        total_bp_df = bp_df[x].value_counts().reset_index().sort_values("index")
        xs = set(total_bp_df["index"].values)
        xs_diff = all_xs.difference(xs)
        if len(xs_diff) !=0:
            add_df = pd.DataFrame(index = range(len(xs_diff)), data = np.transpose([list(xs_diff), [0]*len(xs_diff)]), columns = ["index", x])
            total_bp_df = pd.concat([total_bp_df, add_df]).sort_values("index")
            total_bp_df[x] = total_bp_df[x].astype(int)
                          
        sns.barplot(y = x, x = "index", data = total_bp_df, color = color, order = x_order)

        bp_df = bp_df.loc[bp_df[y]!=an]
    plt.show()
