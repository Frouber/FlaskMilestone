from flask import Flask, render_template, request, redirect
import quandl
import bokeh.io, bokeh.plotting, bokeh.models
from bokeh.plotting import figure
from bokeh.embed import components 
from bokeh.models import LinearAxis,Range1d
import datetime
from dateutil.relativedelta import relativedelta

app = Flask(__name__)

quandl.ApiConfig.api_key = 'xomvruK1ZNabrSwxkJkW'
quandl.ApiConfig.api_version = '2015-04-09'

def get_graph(symbol):
	data = quandl.get('WIKI/'+symbol)

	# get current date and last month
	now = datetime.datetime.now()
	start_period = now-relativedelta(months=2)
	now_str = now.strftime("%Y-%m-%d")
	start_period_str = start_period.strftime("%Y-%m-%d")

	previous = data.loc[data.index > start_period_str]

	# plot last month closing price
	p = figure(x_axis_type="datetime")
	p.line(previous.index, previous.Close)
	p.yaxis.axis_label = 'Price $'
	p.y_range = Range1d(0.95*min(previous.Close), 1.05*max(previous.Close))
	p.extra_y_ranges = {"Volume": Range1d(start=0, end=1.5*max(previous.Volume))}
	p.add_layout(LinearAxis(y_range_name="Volume", axis_label="Volume $"), 'right')
	p.rect(previous.index, y= previous.Volume/2, width=3, height=previous.Volume/1,y_range_name='Volume', color="#CAB2D6")
	p.title = 'Stock price for '+symbol
	p.xaxis.axis_label = 'Date'

	print previous['Close'][0]
	script,div = components(p)
	return script,div

@app.route('/')
def main():
  return redirect('/index')

@app.route('/index', methods=['GET','POST'])
def index():
	if request.method == 'GET':
		return render_template('index.html')
	else:
		symbol = request.form['ticker'].upper()
		print symbol
		script,div = get_graph(symbol)
		return render_template('graph.html', name=symbol, script=script, div=div)
  
if __name__ == '__main__':
  app.run(port=33507)
