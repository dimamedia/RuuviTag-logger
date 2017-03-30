#!/usr/bin/python3

from flask import Flask, render_template
from datetime import datetime, timedelta
import sqlite3
import json
import random

app = Flask(__name__)

def randomRGB():
    r, g, b = [random.randint(0,255) for i in range(3)]
    return r, g, b, 1


@app.route('/')
def index():
	conn = sqlite3.connect("ruuvitag.db")
	conn.row_factory = sqlite3.Row

	# set hom many days you want to see in charts
	N = 30 # show charts for 30 days
	
	date_N_days_ago = str(datetime.now() - timedelta(days=N))
	tags = conn.execute("SELECT DISTINCT mac, name FROM sensors WHERE timestamp > '"+date_N_days_ago+"' ORDER BY name, timestamp DESC")

	sensors = ['temperature', 'humidity', 'pressure']

	sList = {}
	datasets = {}
	for sensor in sensors:
		datasets[sensor] = []

	for tag in tags:
		if tag['name']:
			sList['timestamp'] = []
			for sensor in sensors:
				sList[sensor] = []

			sData = conn.execute("SELECT timestamp, temperature, humidity, pressure FROM sensors WHERE mac = '"+tag['mac']+"' AND timestamp > '"+date_N_days_ago+"' ORDER BY timestamp")
			for sRow in sData:
				sList['timestamp'].append(str(sRow['timestamp'])[:-3]) # remove seconds from timestamp
				for sensor in sensors:
					sList[sensor].append(sRow[sensor])

			color = randomRGB()
			
			dataset = """{{
				label: '{}',
				borderColor: 'rgba{}',
				fill: false,
		        lineTension: 0.2,
				data: {}
			}}"""
			for sensor in sensors:
				datasets[sensor].append(dataset.format(tag['name'], color, sList[sensor]))

	conn.close()
	return render_template('ruuvitag.html', time = sList['timestamp'], temperature = datasets['temperature'], humidity = datasets['humidity'], pressure = datasets['pressure'])

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int('80'))
