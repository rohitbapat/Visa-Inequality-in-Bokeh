# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 01:24:12 2019

@author: rohit
"""
import pandas as pd
from bokeh.models.annotations import Title
from bokeh.models.widgets import Select
from bokeh.layouts import row,column
from bokeh.models import ColumnDataSource,MultiLine,HoverTool,Circle
from bokeh.plotting import figure, curdoc,show
from bokeh.palettes import Viridis10,RdYlBu7,RdGy7
from bokeh.models.widgets import CheckboxGroup,Slider
from bokeh.models.callbacks import CustomJS
import time

income_data = pd.read_json("D:\\DataViz\\Project\\visa-free-travel\\cleandata.json")
result_df = pd.read_csv('country_rank_score.csv')
scatter_countries = pd.merge(result_df[['score','rank','year','country_name']],income_data[['country_name','gdp_percapita','incoming','outgoing']],on='country_name',how='left')

scatter_countries.dropna(inplace=True)

source_gdp = ColumnDataSource({'x': scatter_countries[scatter_countries.year==2006]['rank'].tolist(), 'y': scatter_countries[scatter_countries.year==2006].gdp_percapita.tolist(),'y2': scatter_countries[scatter_countries.year==2006].incoming.tolist(),'year': scatter_countries[scatter_countries.year==2006]['year'].tolist()})

def update_gdp():
    global scatter_countries
    for yr in list(scatter_countries.year.unique()):
        time.sleep(2)
        new = {'x': scatter_countries[scatter_countries.year==yr]['rank'].tolist(),
               'y': scatter_countries[scatter_countries.year==yr].gdp_percapita.tolist(),
               'y2':scatter_countries[scatter_countries.year==yr].incoming.tolist(),
               'year':scatter_countries[scatter_countries.year==yr].year()}
        new = ColumnDataSource(new)
        source_gdp.data.update(new.data)

def gdp_income(result_df,scatter_countries,source_gdp):    
    p3 = figure(plot_width=400, plot_height=400,x_range=(0,110),x_axis_label='Rank',y_axis_label='GDP')
    p3.circle(source=source_gdp, x='x', y='y', size=5,color=RdYlBu7[0])
    t = Title()
    t.text = 'Rank vs GDP'
    p3.title = t
    p3.xaxis.axis_label = 'Rank'
    p3.yaxis.axis_label = 'GDP'
    p2 = figure(plot_width=400, plot_height=400,x_range=(0,110),x_axis_label='Rank',y_axis_label='Incoming Count')
    p2.circle(source=source_gdp, x='x', y='y2', size=5,color=RdYlBu7[6])
    t = Title()
    t.text = 'Rank vs Incoming'
    p2.title = t
    p2.xaxis.axis_label = 'Rank'
    p2.yaxis.axis_label = 'Income'
    
    #t = Title()
    #t.text = 'Rank vs Incoming Count'
    #p2.title = t
    #t = Title()
    #t.text = str(source_gdp.data['year'][0])
    #p2.title = t 
    #source_incoming = ColumnDataSource({'x': scatter_countries[scatter_countries.year==2006]['rank'].tolist(), 'y': scatter_countries[scatter_countries.year==2006].incoming.tolist()})
    #
    #def update_incoming():
    #    global scatter_countries
    #    for yr in list(scatter_countries.year.unique()):
    #        time.sleep(2)
    #        new = {'x': scatter_countries[scatter_countries.year==yr]['rank'].tolist(),
    #               'y': scatter_countries[scatter_countries.year==yr].incoming.tolist()}
    #        new = ColumnDataSource(new)
    #        source_incoming.data.update(new.data)
    #p2 = figure(plot_width=400, plot_height=400,x_range=(0,110))
    #p2.circle(source=source_incoming, x='x', y='y', size=5,color=RdYlBu7[6])
    
    #p = figure(plot_width=400, plot_height=400)
    
    # add a circle renderer with a size, color, and alpha
    #p.circle(scatter_countries[scatter_countries.year==2006]['rank'].tolist(), scatter_countries[scatter_countries.year==2006]['gdp_percapita'].tolist(), size=5, color="navy")
    
    # show the results
    #show(p)
    return p3,p2
    #curdoc().add_root(layout)
    #curdoc().add_periodic_callback(update_gdp, 2000)
#curdoc().add_root(gdp_income())
#curdoc().add_periodic_callback(update_gdp, 500)
