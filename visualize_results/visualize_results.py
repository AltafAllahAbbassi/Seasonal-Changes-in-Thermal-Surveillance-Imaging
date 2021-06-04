# -*- coding: utf-8 -*-
"""
Created on Mon May 31 08:05:44 2021

@author: IvanTower
"""

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns

import os
import sys

from statsmodels.tsa.seasonal import seasonal_decompose

path = os.path.join(os.path.dirname(__file__), os.pardir)

if path not in sys.path:
    sys.path.append(path)


from pre_processing.augment_results import augment_dataframe



# from loaders.pytorch_lightning.dataset import Dataset



def calculate_trend(df, column = "MSE", decomp_freq = 30):
    trend_df = None
    
    for model in models:
        
        df_curr = df[df["model"] == model]
        decomposition = seasonal_decompose(df_curr[column], freq=decomp_freq) 
        trend_ = decomposition.trend
        
        if trend_df is None:
            trend_df = trend_
        else:
            trend_df = trend_df.append(trend_)
            
    return trend_df


def plot_error_vs_other(df, columns, save_dir, smooth = False, decomp_freq = 30):
    #sns.scatterplot(data=df, x="DateTime", y="MSE", hue="model")
    
    if smooth:
        smooth_column = calculate_trend(df, column = columns[1], decomp_freq = decomp_freq)
        df["smooth"] = smooth_column
        old_column = columns[1]
        columns[1] = "smooth"
        
        
    if "DateTime" in columns:
        df["DateTime"] = pd.to_datetime(df['DateTime'], dayfirst = True).dt.strftime('%m-%d')
    
    f, ax = plt.subplots(figsize=(10, 5))
    pl = sns.lineplot(ax = ax, data=df, x=columns[0], y=columns[1], hue="model")

    pl.xaxis.set_major_locator(ticker.MultipleLocator(15))
    plt.xticks(rotation=45)

    plt.show()
    
    if smooth:
        save_dir = os.path.join(save_dir,f'plot_{columns[0]}_{old_column}_smoothed.png')
    else:
        save_dir = os.path.join(save_dir,f'plot_{columns[0]}_{columns[1]}.png')
    
    plt.savefig(save_dir)
    
    
    
def calculate_correlation_mat(df,save_dir):
    f, ax = plt.subplots(figsize=(10, 10))
    
    df = df.drop(['Folder name', 'Image Number'], axis=1)
    
    heatmap = sns.heatmap(df.corr(),ax = ax, vmin=-1, vmax=1, annot=True)
    heatmap.set_title("Correlation Matrix")
    plt.show()
    
    save_dir = os.path.join(save_dir,'correlation_matrix.png')
    
    plt.savefig(save_dir)
    
    
def calculate_depended_value_corr(df,save_dir):
    f, ax = plt.subplots(figsize=(8, 12))
    
    df = df.drop(['Folder name', 'Image Number'], axis=1)
    
    heatmap = sns.heatmap(df.corr()[['MSE']].abs().sort_values(by='MSE', ascending=False),ax = ax, vmin=0, vmax=1, annot=True, cmap='BrBG')
    heatmap.set_title('Features Correlating with MSE', fontdict={'fontsize':18}, pad=16)
    
    save_dir = os.path.join(save_dir,'dependent_value_correlation.png')
    
    plt.savefig(save_dir)
    
    
def plot_barplots(df, columns,save_dir):
    
    f, ax = plt.subplots(figsize=(10, 5))
    bp = sns.barplot(ax = ax, x=columns[0], y=columns[1], data=df, hue="model")
    
    plt.xticks(rotation=45)

    plt.show()
    
    save_dir = os.path.join(save_dir,f'barplot_{columns[0]}_{columns[1]}.png')
    
    plt.savefig(save_dir)
    



if __name__ == '__main__':
    
    method_folder = "CAE"
    
    models = ['feb_day', 'feb_week', 'feb_month']
    months = ['results_jan', 'results_apr', 'results_aug']

    df = None
    for model in models:

        for month in months:
            path = os.path.join(method_folder,model,month+'.csv')

            df_ = pd.read_csv(path)
            # df_["DateTime"] = pd.to_datetime(df_['DateTime'], dayfirst = True).dt.strftime('%m-%d')
            df_["DateTime"] = pd.to_datetime(df_['DateTime'], dayfirst = True)

            df_['model'] = model
            df_['month'] = month

            if df is None:
                df = df_
            else:
                df = df.append(df_)
                
                
    save_folder = os.path.join(method_folder,"results")
    if not os.path.exists(save_folder):

        os.makedirs(save_folder)
    
   
    df = augment_dataframe(df)
    
    # calculate_correlation_mat(df,save_folder)
                
    # calculate_depended_value_corr(df, save_folder)
    
    # plot_error_vs_other(df,["Temperature", "MSE"],save_folder,smooth = False)
    
    # plot_error_vs_other(df,["Humidity", "MSE"],save_folder,smooth = False)
             


    # plot_barplots(df, ["Hour", "MSE"], save_folder)    
    
    # plot_barplots(df, ["Day_Night", "MSE"], save_folder)   
    
    # plot_barplots(df, ["Timeslot_name", "MSE"], save_folder)
    
    # plot_barplots(df, ["Weekday_name", "MSE"], save_folder)   
                