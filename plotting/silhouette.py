import seaborn as sns
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import silhouette_sample, silhouette_score


def plot_silhouettes(df, labels, avg_line=True, save_file=None):
    '''
    Plot silhouette scores of pre-generated clustering labels

    df - pandas DataFrame of data from which clusters were generated
    labels - pandas DataFrame of pregenerated labels per sample

    Plots silhouette scores by cluster label and saves plot if given path
    '''


