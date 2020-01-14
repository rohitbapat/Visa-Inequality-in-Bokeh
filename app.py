# -*- coding: utf-8 -*-
"""
Created on Sat Nov 30 22:40:36 2019

@author: rohit
"""

from bokeh.server.server import Server
from bokeh.application import Application
from bokeh.application.handlers.function import FunctionHandler
from bokeh.plotting import figure, ColumnDataSource
from bokeh.io import output_file, show,curdoc
from bokeh.models.widgets import CheckboxGroup
from bokeh.layouts import row
from bokeh.models import HoverTool,CDSView,GroupFilter
from bokeh.palettes import Category10
import bokeh.plotting as bp
import pandas as pd

def make_data(country_list,country_rank_df):

    p = figure(plot_width=600, plot_height=600)
    
    for i in range(len(country_list)):
        
        data = bp.ColumnDataSource(data={'year':country_rank_df.loc[country_rank_df.country_name == country_list[i]].year,
           'group':country_rank_df.loc[country_rank_df.country_name == country_list[i]].country_name,
           'score':country_rank_df.loc[country_rank_df.country_name == country_list[i]].score})
        
        view=CDSView(source=data,filters=[GroupFilter(column_name='country_name', group=country_list[i])])
        
        p.line('year','score',source=data,view=view, line_width=2,color = (Category10[3])[i],legend = country_list[i])

    hover = HoverTool(tooltips=[('Score', '@score')])
    
    checkbox_group = CheckboxGroup(labels=list(country_rank_df.country_name.unique()),active = [0, 1])

    p.add_tools(hover)
    
    layout = row(p,checkbox_group)
    
    return layout

def make_document(doc):
    country_rank_df = pd.read_csv("D:\\DataViz\\Project\\country_rank_score.csv")
    country_list = ['Denmark']
    layout = make_data(country_rank_df,country_list)
    doc.add_root(layout)
    
    
apps = {'/': Application(FunctionHandler(make_document))}

server = Server(apps, port=5006)
server.start()
#server.stop()
