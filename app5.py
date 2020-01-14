# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 17:44:19 2019

@author: rohit
"""
import pandas as pd
from bokeh.models.widgets import Select
from bokeh.layouts import row,column
from bokeh.models import ColumnDataSource,MultiLine,HoverTool
from bokeh.plotting import figure, curdoc,show
from bokeh.palettes import Viridis10,RdYlBu7,RdGy7
from bokeh.models.widgets import CheckboxGroup,Slider
from bokeh.models.callbacks import CustomJS

def get_bar():
    country_rank_df = pd.read_csv("D:\\DataViz\\Project\\country_rank_score.csv")
    country_rank_df.dropna(inplace=True)
    
    country_rank_df_2006 = country_rank_df[country_rank_df.year==2006].sort_values('country_name')[['rank','score','country_name']]
    country_rank_df_2019 = country_rank_df[country_rank_df.year==2019].sort_values('country_name')[['rank','score','country_name']]
    difference_df = pd.merge(country_rank_df_2006,country_rank_df_2019,on='country_name',how='left')
    winners_index = (difference_df['rank_x'] - difference_df['rank_y']).sort_values().index[-5:]
    losers_index = (difference_df['rank_x'] - difference_df['rank_y']).sort_values().index[:5]
    
    difference_df['rank_diff'] = difference_df['rank_x'] - difference_df['rank_y']
    
    source = ColumnDataSource(difference_df.loc[winners_index])
    
    hover = HoverTool(tooltips=[("Score@2006", "@score_x"),
        ('Score@2019', '@score_y')])
    
    p2 = figure(x_range=difference_df.loc[winners_index].country_name, plot_height=350,plot_width=700, title="Biggest Climbers since 2006",
                tools="")
    p2.vbar(x='country_name', top='rank_diff', width=0.5,source=source,fill_color=Viridis10[0])
    
    p2.y_range.start = 0
    p2.add_tools(hover)
    p2.xaxis.axis_label = 'Countries'
    p2.yaxis.axis_label = 'Rank Difference'
    
    source = ColumnDataSource(difference_df.loc[losers_index])
    
    p3 = figure(x_range=difference_df.loc[losers_index].country_name, plot_height=350,plot_width=700, title="Biggest Fallers since 2006",
               toolbar_location=None, tools="")
    p3.vbar(x='country_name', top='rank_diff', width=0.5, source=source,fill_color=Viridis10[6])
    p3.y_range.start = -40
    p3.y_range.end = 0
    hover = HoverTool(tooltips=[("Score 2006", "@score_x"),
        ('Score 2019', '@score_y')])
    p3.add_tools(hover)
    p3.xaxis.axis_label = 'Countries'
    p3.yaxis.axis_label = 'Rank Difference'
    bar_layout = column(p2,p3)
    
    return bar_layout