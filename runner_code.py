# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 17:46:55 2019

@author: rohit
"""

import pandas as pd
from functools import partial
from bokeh.models.widgets import Select
from bokeh.models.annotations import Title
from bokeh.layouts import row,column
from bokeh.models import ColumnDataSource,MultiLine,HoverTool
from bokeh.plotting import figure, curdoc,show,save,output_file
from bokeh.palettes import Viridis10,RdYlBu7,RdGy7
from bokeh.models.widgets import CheckboxGroup,Slider
from bokeh.models.callbacks import CustomJS
from app4 import top_countries
from app5 import get_bar
from app3 import gdp_income
from shape.app6 import get_plot
from bokeh.models.widgets import Tabs, Panel
import time

income_data = pd.read_json("D:\\DataViz\\Project\\visa-free-travel\\cleandata.json")
result_df = pd.read_csv('country_rank_score.csv')
scatter_countries = pd.merge(result_df[['score','rank','year','country_name']],income_data[['country_name','gdp_percapita','incoming','outgoing']],on='country_name',how='left')

scatter_countries.dropna(inplace=True)

source_gdp = ColumnDataSource({'x': scatter_countries[scatter_countries.year==2006]['rank'].tolist(), 'y': scatter_countries[scatter_countries.year==2006].gdp_percapita.tolist(),'y2': scatter_countries[scatter_countries.year==2006].incoming.tolist(),'year': scatter_countries[scatter_countries.year==2006]['year'].tolist()})

country_rank_df = pd.read_csv("D:\\DataViz\\Project\\country_rank_score.csv")
country_rank_df.dropna(inplace=True)

def update_gdp():
    global scatter_countries
    for yr in list(scatter_countries.year.unique()):
        time.sleep(2)
        new = {'x': scatter_countries[scatter_countries.year==yr]['rank'].tolist(),
               'y': scatter_countries[scatter_countries.year==yr].gdp_percapita.tolist(),
               'y2':scatter_countries[scatter_countries.year==yr].incoming.tolist(),
               'year':scatter_countries[scatter_countries.year==yr].year.tolist()}
        new = ColumnDataSource(new)
        p2.title.text = 'Rank vs Incoming'
        p3.title.text = 'Rank vs GDP'
        p2.title.text = p2.title.text + ' Year ' + str(new.data['year'][0])
        p3.title.text = p3.title.text + ' Year ' + str(new.data['year'][0])
        source_gdp.data.update(new.data)
        
def get_all_price_dataset(country_rank_df,names):
        df = dict()
        df['year'] = []
        df['score'] = []
        df['color'] = []
        df['country'] = []
        for ind,country in enumerate(names):
            df['year'].append(country_rank_df[(country_rank_df.country_name == country)].year.tolist())
            df['score'].append(country_rank_df[(country_rank_df.country_name == country)].score.tolist())
            df['color'].append(RdYlBu7[ind])
            df['country'].append(country)
        return df
start_df = get_all_price_dataset(country_rank_df,['Denmark'])
    #DisplayData = ColumnDataSource(dict('year1'= [country_rank_df[country_rank_df.country_name=='Denmark'].year.tolist()],'score1'=[country_rank_df[country_rank_df.country_name=='Denmark'].score.tolist()]))
DisplayData = ColumnDataSource(start_df)


layout1 = get_bar()
layout2 = top_countries(country_rank_df)
p3,p2 = gdp_income(result_df,scatter_countries,source_gdp)
layout3 = row(p3,p2)
p4,p5,p6,p7,p8 = get_plot()

tab1 = Panel(child=layout1,title="Country Comparison")
tab2 = Panel(child=layout2,title="Top Climbers/Top Fallers")
tab3 = Panel(child=layout3,title="GDP Incoming Rank vs. Rank Relation")
tab4 = Panel(child=p4,title="Score Comparison")
tab5 = Panel(child=p5,title="GDP Per Capita with Score")
tab6 = Panel(child=p6,title="Incoming vs Outgoing Rates")
tab7 = Panel(child=p7,title="Where Can I travel to?")
tab8 = Panel(child=p8,title="Highlighting Differences")

tabs = Tabs(tabs=[tab1,tab2,tab4,tab5,tab6,tab7,tab8,tab3])

call_back_obj = False

def panelActive(attr, old, new):
    global call_back_obj
    if tabs.active == 7:
        call_back_obj = curdoc().add_periodic_callback(update_gdp,2000)
    elif tabs.active!=7 and call_back_obj:
        curdoc().remove_periodic_callback(call_back_obj)
        call_back_obj = False

#curdoc().add_root(tabs)
save(tabs)
output_file("output.html",title='runner_code.py example')
tabs.on_change('active', panelActive)


