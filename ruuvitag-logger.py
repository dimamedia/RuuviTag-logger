#!/usr/bin/python3

import time
from ruuvitag_sensor.ble_communication import BleCommunicationNix
from ruuvitag_sensor.ruuvi import RuuviTagSensor
from ruuvitag_sensor.url_decoder import UrlDecoder

ble = BleCommunicationNix()

# list all your tags MAC: TAG_NAME
tags = {
    'CC:CA:7E:52:CC:34': '1: Backyard',
    'FB:E1:B7:04:95:EE': '2: Upstairs',
    'E8:E0:C6:0B:B8:C5': '3: Downstairs'
}

# set DataFormat
# 1 - Weather station
# 3 - SensorTag data format 3 (under development)
dataFormat = '1'

dweet = True # Enable or disable dweeting True/False
dweetUrl = 'https://dweet.io/dweet/for/' # dweet.io url
dweetThing = 'myHomeAtTheBeach' # dweet.io thing name

db = True # Enable or disable database saving True/False
dbFile = '/home/pi/ruuvitag/ruuvitag.db' # path to db file

if dweet:
	import requests
'''
Dweet format:
{
	'TAG_NAME1 temperature': VALUE,
	'TAG_NAME1 humidity': VALUE,
	'TAG_NAME1 pressure': VALUE,
	'TAG_NAME2 temperature': VALUE,
	'TAG_NAME2 humidity': VALUE,
	'TAG_NAME2 pressure': VALUE,
	etc...
}
'''

if db:
	import sqlite3
	# open database
	conn = sqlite3.connect(dbFile)

	# check if table exists
	cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='sensors'")
	row = cursor.fetchone()	
	if row is None:
		print("DB table not found. Creating 'sensors' table ...")
		conn.execute('''CREATE TABLE sensors
			(
				id				INTEGER		PRIMARY KEY AUTOINCREMENT	NOT NULL,
				timestamp		NUMERIC		DEFAULT CURRENT_TIMESTAMP,
				mac				TEXT		NOT NULL,
				name			TEXT		NULL,
				temperature		NUMERIC		NULL,
				humidity		NUMERIC		NULL,
				pressure		NUMERIC		NULL
			);''')
		print("Table created successfully\n")

# Extended RuuviTagSensor with name, and raw data output
class Rtag(RuuviTagSensor):

	def __init__(self, mac, name):
		self._mac = mac
		self._name = name

	@property
	def name(self):
		return self._name

	def getData(self):
		return ble.get_data(self._mac)

	
now = time.strftime('%Y-%m-%d %H:%M:%S')
print(now+"\n")

dweetData = {}
dbData = {}
	
for mac, name in tags.items():
	tag = Rtag(mac, name)

	print("Looking for {} ({})".format(tag._name, tag._mac))
	# if weather station
	if dataFormat == '1': # get parsed data

		data = UrlDecoder().decode_data(RuuviTagSensor.convert_data(tag.getData()))
		print ("Data received:", data)

		dbData[tag._mac] = {'name': tag._name}
		# add each sensor with value to the lists
		for sensor, value in data.items():
			dweetData[tag._name+' '+sensor] = value
			dbData[tag._mac].update({sensor: value})

	elif dataFormat == '3': # under development
		print ("Data:", tag.getData())
		
	else: # if unknown format, just print raw data
		print ("Data:", tag.getData())

	print("\n")
		
if dweet:
	# send data to dweet.io
	print("Dweeting data for {} ...".format(dweetThing))
	response = requests.post(dweetUrl+dweetThing, json=dweetData)
	print(response)
	#print(response.text)

if db:
	# save data to db
	print("Saving data to database ...")
	for mac, content in dbData.items():
		conn.execute("INSERT INTO sensors (timestamp,mac,name,temperature,humidity,pressure) \
			VALUES ('{}', '{}', '{}', '{}', '{}', '{}')".\
			format(now, mac, content['name'], content['temperature'], content['humidity'], content['pressure']))
	conn.commit()
	conn.close()
	print("Done.")
