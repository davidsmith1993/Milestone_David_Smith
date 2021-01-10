# -*- coding: utf-8 -*-
"""
Created on Sat Dec 26 21:04:41 2020

@author: dsmit
"""


from flask import Flask, render_template, request, redirect
#"""
import alpha_vantage
import requests


from bokeh.layouts import row, column, widgetbox
from bokeh.plotting import figure, show, output_file, ColumnDataSource
from bokeh.models.widgets import Select
from bokeh.io import curdoc, show

import pandas as pd
from bokeh.layouts import row
from bokeh.io import output_file, show
from bokeh.plotting import figure, save
from bokeh.models import HoverTool, ColumnDataSource
from bokeh.models.widgets import Dropdown
from bokeh.palettes import Spectral5
from bokeh.transform import factor_cmap
from bokeh.transform import dodge
from bokeh.models import ColumnDataSource, Select
from bokeh.io import curdoc
from alpha_vantage.timeseries import TimeSeries
from bokeh.embed import components 
from bokeh.io import output_file, show





def fetch(ticker) :
    ticker=ticker.upper()
    

    ts = TimeSeries(key='MO8BPQU6ZKVP11BJ',output_format='pandas')
    data, meta_data = ts.get_intraday(ticker)    
    data['date'] = data.index
    data2, meta_data2 = ts.get_daily_adjusted(ticker)    
    data2['date'] = data.index
     
    return(data, data2)








def make_figure(data, data2):
    p=figure(x_axis_type="datetime", width=400, height=300)
    if request.form.get('Close'):
        p.line(x=data['date'].values, y=data['4. close'].values,line_width=1.8, legend='Close')
    if request.form.get('Adj. Close'):
        p.line(x=data2['date'].values, y=data2['5. adjusted close'].values,line_width=1.8, line_color="orange", legend='Adj. Close')
    if request.form.get('Open'):
        p.line(x=data['date'].values, y=data['1. open'].values,line_width=1.8, line_color="black", legend='Open')
    if request.form.get('Adj. Open'):
        p.line(x=data2['date'].values, y=data2['1. open'].values,line_width=1.8, line_color="blue", legend='Adj. Open')
    
    
    p.xaxis.axis_label = 'Date'
    p.yaxis.axis_label = 'Price'



    p.grid.grid_line_alpha=0.3
    

    output_file('templates/plot.html')
    save(p)
    script, div=components(p)
    return(script, div)




app = Flask(__name__)

app.vars = {}



@app.route('/')
def index():
  return render_template('index_test_lines.html')


@app.route('/plotpage', methods=['POST'])
def plotpage():
    tickStr=request.form['tickerText']
    
    app.vars['ticker']=tickStr.upper()
    data, data2 =fetch(app.vars['ticker'])
    script,div=make_figure(data, data2)
    return render_template('plot.html', script=script, div=div)



if __name__ == '__main__':
    app.run(port=33507)

