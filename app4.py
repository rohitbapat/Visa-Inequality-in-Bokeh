# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 17:17:56 2019

@author: rohit
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Dec  1 18:28:31 2019

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
'''
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

source = ColumnDataSource(difference_df.loc[losers_index])

p3 = figure(x_range=difference_df.loc[losers_index].country_name, plot_height=350,plot_width=700, title="Biggest Fallers since 2006",
           toolbar_location=None, tools="")
p3.vbar(x='country_name', top='rank_diff', width=0.5, source=source,fill_color=Viridis10[6])
p3.y_range.start = -40
p3.y_range.end = 0
hover = HoverTool(tooltips=[("Score 2006", "@score_x"),
    ('Score 2019', '@score_y')])
p3.add_tools(hover)
bar_layout = column(p2,p3)
#show(layout)
'''

def top_countries(country_rank_df):
    
    menu = Select(options=['Top Seven','Bottom Seven'], value='Top Seven',title='Select Type')
    
    #country_selection = CheckboxGroup(labels=sorted(list(country_rank_df.country_name.unique())), 
    #                                  active = [0])
    
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
    
    start_df = get_all_price_dataset(country_rank_df,['United Arab Emirates','Albania','Taiwan (Chinese Taipei)','Bosnia and Herzegovina','Serbia','Bosnia and Herzegovina','Colombia'])
    #DisplayData = ColumnDataSource(dict('year1'= [country_rank_df[country_rank_df.country_name=='Denmark'].year.tolist()],'score1'=[country_rank_df[country_rank_df.country_name=='Denmark'].score.tolist()]))
    DisplayData = ColumnDataSource(start_df)
    
    col_layout = column(menu)
    
    p = figure(plot_width=600, plot_height=600,y_range=(10,200))
    #numlines = len([country_selection.labels[i] for i in country_selection.active])
    #mypalette=Viridis10[0:numlines]
    #p.line(x='year',y='score',source=DisplayData,color=Viridis10[0])
    p.multi_line(xs='year',ys='score',source=DisplayData,line_color='color',legend='country')
    p.xaxis.axis_label = 'Year'
    p.yaxis.axis_label = 'Score'
    #action_callback = CustomJS(args=dict(country_selection=country_selection, col_layout=col_layout, menu=menu),code="""
    #var action = menu.value;
    #if (action == 'Select Countries') {
    #col_layout.children = [menu,country_selection];
    #} else {
    #col_layout.children = [menu];
    #}
    #window.alert(col_layout.children);
    #""")
    
    def update_plot(attrname, old, new):
        if menu.value == 'Top Seven':
            newccy = ['United Arab Emirates','Albania','Taiwan (Chinese Taipei)','Bosnia and Herzegovina','Serbia','Bosnia and Herzegovina','Colombia']
        else:
            newccy = ['Nigeria','Sierra Leone','Bangladesh','Syria','Mali','Niger','Senegal']
        #newccy = [country_selection.labels[i] for i in country_selection.active]
        
        src_data_table = ColumnDataSource(get_all_price_dataset(country_rank_df,newccy))
        
        DisplayData.data.update(src_data_table.data)
        #On change in menu,function gets called.
    
    #menu.js_on_change('value', action_callback) 
        
        
    menu.on_change('value', update_plot)
    #country_selection.on_change('active',update_plot)
    
    
        #Displaying Menu and Plot.
    
    #p.line(x='year',y='score',source=DisplayData,color=Viridis10[1],size=6)
    
    #col_layout = column(country_selection)
    #layout = row(country_selection,p)
    #return menu,p
    layout = column(col_layout,p)
    #show(layout)
    #final_layout = row(layout)
    #final_layout = layout
    #curdoc().add_root(final_layout)
    return layout

#country_rank_df = pd.read_csv("D:\\DataViz\\Project\\country_rank_score.csv")
#country_rank_df.dropna(inplace=True)
#ly = top_countries(country_rank_df)
#curdoc().add_root(ly)






