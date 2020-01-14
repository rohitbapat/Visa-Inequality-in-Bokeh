# -*- coding: utf-8 -*-
"""
Created on Fri Dec  6 00:51:00 2019

@author: rohit
"""

import altair as alt
import pandas as pd
# saving data into a file rather than embedding into the chart
alt.data_transformers.enable('json') 
# alt.renderers.enable('notebook')
# !pip install geopandas
import geopandas as gpd
import json
# !pip install bokeh==1.1
from bokeh.io import output_notebook, show, output_file
from bokeh.plotting import figure
from bokeh.models import GeoJSONDataSource, LinearColorMapper, ColorBar
from bokeh.palettes import brewer
from bokeh.models import Slider, HoverTool
from bokeh.models import ColumnDataSource, CategoricalColorMapper
from bokeh.palettes import RdYlBu5,RdGy5
import random
from bokeh.models.widgets import CheckboxGroup
from bokeh.models.widgets import Select
from bokeh.plotting import figure, curdoc,show
from bokeh.layouts import column, row, WidgetBox
from bokeh.models import Panel
from bokeh.models.widgets import Tabs
from bokeh.models.widgets import CheckboxGroup
from shapely.geometry import Point, LineString, Polygon
from bokeh.models.widgets import Select
import pandas as pd
from bokeh.layouts import widgetbox, row, column


data_visatype = pd.read_csv('D:\DataViz\Project\shape\country_preprocessed.csv')
data_years_data=pd.read_csv('D:\DataViz\Project\shape\country_rank_score.csv')
centroid_data=pd.read_csv("D:\DataViz\Project\country_centroids_az8.csv")
income_gdp=pd.read_csv('D:\DataViz\Project\shape\IncomingGDPData.csv')
hd=pd.read_csv('D:\DataViz\Project\shape\highlight differences.csv')

sub_rank_2018=data_years_data[data_years_data['year']==2018]

shapefile = 'D:\DataViz\Project\shape\\ne_110m_admin_0_countries.shp'

def get_plot():
    #Read shapefile using Geopandas
    gdf = gpd.read_file(shapefile)[['ADMIN', 'ADM0_A3', 'geometry']]
    #Rename columns.
    gdf.columns = ['country', 'country_code', 'geometry']
    
    merged = gdf.merge(sub_rank_2018, left_on='country_code',right_on='code',how='inner')
    
    #Read data to json.
    merged_json = json.loads(merged.to_json())
    #Convert to String like object.
    json_data = json.dumps(merged_json)
    
    geosource = GeoJSONDataSource(geojson = json_data)
    #Define a sequential multi-hue color palette.
    palette = brewer['YlGnBu'][8]
    #Reverse color order so that dark blue is highest score.
    palette = palette[::-1]
    #Instantiate LinearColorMapper that linearly maps numbers in a range, into a sequence of colors.
    color_mapper = LinearColorMapper(palette = palette, low = 0, high = 190)
    #Define custom tick labels for color bar.
    tick_labels = {'1': '30', '2': '50', '3':'80', '4':'100', '5':'120', '6':'150', '7':'>190+'}
    #Create color bar. 
    color_bar = ColorBar(color_mapper=color_mapper, label_standoff=8,width = 500, height = 20,
    border_line_color=None,location = (0,0), orientation = 'horizontal', major_label_overrides = tick_labels)
    
    #Add hover tool
    hover = HoverTool(tooltips = [ ('Country/region','@country'),('% score', '@score')])
    
    #Create figure object.
    p = figure(title = 'Travel visa Inequality Score', plot_height = 600 , plot_width = 950, toolbar_location = None, tools = [hover])
    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = None
    
    
    
    #Add patch renderer to figure. 
    p.patches('xs','ys', source = geosource,fill_color = {'field' :'score', 'transform' : color_mapper},
              line_color = 'black', line_width = 0.25, fill_alpha = 1)
    #Specify figure layout.
    p.add_layout(color_bar, 'below')
    
    merged2=merged.merge(centroid_data[['gu_a3','Longitude','Latitude']],how='inner',left_on='country_code',right_on='gu_a3')
    merged3=merged2.merge(income_gdp,how='left',left_on='country_code',right_on='code')
    
    merged3['gdp_millions']=merged3['gdp_percapita']/1000000
    merged3['norm_percapita']=(merged3['gdp_percapita']-merged3['gdp_percapita'].min())/(merged3['gdp_percapita'].max()-merged3['gdp_percapita'].min())
    
    merged3['norm_percapita']=merged3['norm_percapita']*40
    
    merged3['norm_outgoing']=(merged3['outgoing']-merged3['outgoing'].min())/(merged3['outgoing'].max()-merged3['outgoing'].min())
    
    merged3['norm_outgoing']=merged3['norm_outgoing']*40
    
    merged3['norm_incoming']=(merged3['incoming']-merged3['incoming'].min())/(merged3['incoming'].max()-merged3['incoming'].min())
    
    merged3['norm_incoming']=merged3['norm_incoming']*40
    
    merged_json = json.loads(merged3.to_json())
    #Convert to String like object.
    json_data = json.dumps(merged_json)
    
    #Input GeoJSON source that contains features for plotting.
    geosource = GeoJSONDataSource(geojson = json_data)
    #Define a sequential multi-hue color palette.
    palette = brewer['YlGnBu'][8]
    #Reverse color order so that dark blue is highest score.
    palette = palette[::-1]
    #Instantiate LinearColorMapper that linearly maps numbers in a range, into a sequence of colors.
    color_mapper = LinearColorMapper(palette = palette, low = 0, high = 190, nan_color = '#d9d9d9')
    #Define custom tick labels for color bar.
    tick_labels = {'1': '30', '2': '50', '3':'80', '4':'100', '5':'120', '6':'150', '7':'>190+'}
    #Create color bar. 
    color_bar = ColorBar(color_mapper=color_mapper, label_standoff=8,width = 500, height = 20,
    border_line_color=None,location = (0,0), orientation = 'horizontal', major_label_overrides = tick_labels)
    
    #Add hover tool
    hover = HoverTool(tooltips = [ ('Country/region','@country'),('% score', '@score'),('GDP(in millions) per capita','@gdp_millions')])
    
    #Create figure object.
    p1 = figure(title = 'Travel visa Inequality Score and GDP', plot_height = 600 , plot_width = 950, toolbar_location = None, tools = [hover])
    p1.xgrid.grid_line_color = None
    p1.ygrid.grid_line_color = None
    
    #Add patch renderer to figure. 
    p1.patches('xs','ys', source = geosource,fill_color = {'field' :'score', 'transform' : color_mapper},
              line_color = 'black', line_width = 0.25, fill_alpha = 1)
    #Specify figure layout.
    p1.add_layout(color_bar, 'below')
    p1.circle('Longitude','Latitude',size='norm_percapita', color="orange", alpha=0.7,source=geosource)


    #Input GeoJSON source that contains features for plotting.
    geosource = GeoJSONDataSource(geojson = json_data)
    #Define a sequential multi-hue color palette.
    palette = brewer['YlGnBu'][8]
    #Reverse color order so that dark blue is highest score.
    palette = palette[::-1]
    #Instantiate LinearColorMapper that linearly maps numbers in a range, into a sequence of colors.
    color_mapper = LinearColorMapper(palette = palette, low = 0, high = 190, nan_color = '#d9d9d9')
    #Define custom tick labels for color bar.
    tick_labels = {'1': '30', '2': '50', '3':'80', '4':'100', '5':'120', '6':'150', '7':'>190+'}
    #Create color bar. 
    color_bar = ColorBar(color_mapper=color_mapper, label_standoff=8,width = 500, height = 20,
    border_line_color=None,location = (0,0), orientation = 'horizontal', major_label_overrides = tick_labels)
    
    #Add hover tool
    hover = HoverTool(tooltips = [ ('Country/Region','@country'),('% Score', '@score'),('Outgoing','@outgoing'),('Incoming','@incoming')])
    
    #Create figure object.
    p2 = figure(title = 'Travel visa inequality score and Incoming/Outgoing People', plot_height = 600 , plot_width = 950, toolbar_location = None, tools = [hover])
    p2.xgrid.grid_line_color = None
    p2.ygrid.grid_line_color = None
    
    #Add patch renderer to figure. 
    p2.patches('xs','ys', source = geosource,fill_color = {'field' :'score', 'transform' : color_mapper},
              line_color = 'black', line_width = 0.25, fill_alpha = 1)
    #Specify figure layout.
    p2.add_layout(color_bar, 'below')
    p2.circle('Longitude','Latitude',size='norm_incoming', color="orange", alpha=0.7,source=geosource)
    p2.circle('Longitude','Latitude',size='norm_outgoing', color="grey", alpha=0.7,source=geosource)
    
    bucket = ['Incoming','Outgoing']
    color_mapper3 = CategoricalColorMapper(factors=bucket, palette=['orange','grey'])
    for factor, color in zip(color_mapper3.factors, color_mapper3.palette):
          p2.circle(x=[], y=[], fill_color=color, legend=factor)
    
    
    def visa_cat(col):
      if col==0:
        return 'Visa Not Required'
      elif col==1:
        return 'Visa On Arrival'
      elif col==2:
        return 'ETA Required'
      elif col==3:
        return 'eVisa Required'
      elif col==4:
        return 'Visa Required'
      elif col==5:
        return 'Admission Refused'

    data_visatype['cat']=data_visatype['visa_type'].apply(visa_cat)
    vis2= gdf.merge(data_visatype, left_on='country_code',right_on='code2',how='inner')
    
    def make_dataset(cat_list):
      subset = vis2[vis2['country1'] == cat_list]
      merged_json1 = json.loads(subset.to_json())
      json_data2 = json.dumps(merged_json1)
      return json_data2

    geosource = GeoJSONDataSource(geojson = make_dataset('Afghanistan'))
    
    def update_plot(attr, old, new):
        # The input yr is the year selected from the slider
        country = select2.value
        new_data = make_dataset(country)
        geosource.geojson = new_data 
        # Update the plot based on the changed inputs
        #p11 = make_plot()
        
        # Update the layout, clear the old document and display the new document
        #layout = column(widgetbox(select),p3)
    #     curdoc().clear()
    #     curdoc().add_root(layout)
        
        # Update the data
        
    def make_plot():
      categ=['Visa Not Required','Visa On Arrival','ETA Required','eVisa Required','Visa Required','Selected Country']
      color_mapper2 = CategoricalColorMapper(factors=categ, palette=[RdYlBu5[0], RdYlBu5[1],RdYlBu5[2],RdYlBu5[3],RdYlBu5[4],RdGy5[0]])
    
      #Define custom tick labels for color bar.
      #tick_labels1 = {'0': 'Visa Not Required', '1': 'Visa On arrival', '3':'ETA Required', '4':'Visa Required', '5':'Admission Refused'}
    
      # #Create color bar. 
      # color_bar = ColorBar(color_mapper=color_mapper2)
      # ColorBar(color_mapper=color_mapper2 , label_standoff=12, location=(0,0))
    
      #Add hover tool
      hover = HoverTool(tooltips = [ ('Country/region','@country'),('travel category', '@cat')])
    
      #Create figure object.
      p11 = figure(title = ('Where can a selected Country Travel to?'), plot_height = 600 , plot_width = 950, toolbar_location = None, tools = [hover])
      p11.xgrid.grid_line_color = None
      p11.ygrid.grid_line_color = None
    
      #Add patch renderer to figure. 
      p11.patches('xs','ys', source = geosource,fill_color = {'field' :'cat', 'transform' : color_mapper2}, line_color = 'black', line_width = 0.25, fill_alpha = 1)
    
      for factor, color in zip(color_mapper2.factors, color_mapper2.palette):
          p11.circle(x=[], y=[], fill_color=color, legend=factor)
      #Specify figure layout.
      return p11
    
    
    p10 = make_plot()
    countries=list(vis2['country1'].unique())
    
    
    select2 = Select(title='Select a Country:', value='Afghanistan', options=countries)
    select2.on_change('value', update_plot)

    layout = column(widgetbox(select2),p10)
    
    
    visa3=vis2[['country_code','geometry']]

    visa4=visa3.drop_duplicates(keep='first', inplace=False)
    
    vis5= visa4.merge(hd, left_on='country_code',right_on='code2',how='inner')
    
    temp_data=vis2[['country1','code1']].drop_duplicates(keep='first',inplace=False)
    
    vis6 = vis5.merge(temp_data[['country1','code1']], on='code1',how='inner')
    
    def adv_tag(col):
        if col==1:
            return 'Advantage'
        elif col==-1:
            return 'Disadvantage'
        elif col==0:
            return 'Neutral'
        else:
            return 'Selected Country'
    
    vis6['tag']=vis6['diff'].apply(adv_tag)
    
    vis6.reset_index(drop=True,inplace=True)
    
    
    def make_dataset_diff(cat_list):
        subset = vis6[vis6['country1'] == cat_list]
        merged_json1 = json.loads(subset.to_json())
        json_data2 = json.dumps(merged_json1)
        return json_data2

    geosource2 = GeoJSONDataSource(geojson = make_dataset_diff('Canada'))

    def update_plot_diff(attr, old, new):
         # The input yr is the year selected from the slider
        country = select.value
        new_data = make_dataset_diff(country)
        geosource2.geojson = new_data 
    #     # Update the plot based on the changed inputs
        #p3 = make_plot_diff()
        
    #     # Update the layout, clear the old document and display the new document
        #layout3 = column(widgetbox(select),p3)
        
    def make_plot_diff():
        tag=['Advantage','Neutral','Disadvantage','Selected Country']
        color_mapper2 = CategoricalColorMapper(factors=tag, palette=[RdYlBu5[0],RdYlBu5[1],RdYlBu5[4],RdGy5[0]])
    
        hover = HoverTool(tooltips = [ ('Country/region','@code2'),('Advantage tag', '@tag')])
        p3 = figure(title = ('Selected Country Travel to?'), plot_height = 600 , plot_width = 950, toolbar_location = None, tools = [hover])
        p3.xgrid.grid_line_color = None
        p3.ygrid.grid_line_color = None
        
        
    #   #Add patch renderer to figure. 
        p3.patches('xs','ys', source = geosource2,fill_color = {'field' :'tag', 'transform' : color_mapper2}, line_color = 'black', line_width = 0.25, fill_alpha = 1)
    
        for factor, color in zip(color_mapper2.factors, color_mapper2.palette):
            p3.circle(x=[], y=[], fill_color=color, legend=factor)
    #   #Specify figure layout.
        return p3

    p4 = make_plot_diff()
    countries=list(vis2['country1'].unique())
    
    
    select = Select(title='Select Country:', value='Canada', options=countries)
    select.on_change('value', update_plot_diff)
    
    layout1 = column(widgetbox(select),p4)
    
    return p,p1,p2,layout,layout1

#p,p1,p2,layout,layout1 = get_plot()
#
#curdoc().add_root(layout)
#show(layout1)
