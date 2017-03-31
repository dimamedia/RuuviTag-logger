# RuuviTag-logger
Log RuuviTags data to SQLite database and Dweet.io and show charts on the RPi's website

**Charts demo:** [https://dima.fi/ruuvitag-logger/](https://dima.fi/ruuvitag-logger/)

## Used elements
  - [Raspberry Pi 3](https://www.raspberrypi.org/products/raspberry-pi-3-model-b/)
  - [Python 3](https://docs.python.org/3.6/)
  - [RuuviTag Sensor Python Package](https://github.com/ttu/ruuvitag-sensor) by [Tomi Tuhkanen](https://github.com/ttu)
  - [Flask microframework](http://flask.pocoo.org/)
  - [SQLite 3 database](https://docs.python.org/3.6/library/sqlite3.html#module-sqlite3)
  - [Dweet.io - IOT dwitter](https://dweet.io)
  - [Chart.js](http://www.chartjs.org/)

## Install

Create `ruuvitag` folder in pi's home:
```bash
$ mkdir /home/pi/ruuvitag
```

Put files like this:

```bash
ruuvitag
 |- ruuvitag-logger.py
 |- ruuvitag-web.py
 |- templates
      |- ruuvitag.html
```

## Setup logger

Edit `ruuvitag-logger.py` file and set desired settings.

List and name your tags:

```python
tags = {
    'CC:CA:7E:52:CC:34': '1: Backyard',
    'FB:E1:B7:04:95:EE': '2: Upstairs',
    'E8:E0:C6:0B:B8:C5': '3: Downstairs'
}
```

Chose RuuviTag's data format:

  - 1 - Weather station firmware
  - 3 - Sensor tag firmware (in development)

```python
dataFormat = '1'
```
  
If you want to use Dweet.io, enable it and set Thing name:

```python
dweet = True # Enable or disable dweeting True/False
dweetUrl = 'https://dweet.io/dweet/for/' # dweet.io url
dweetThing = 'myHomeAtTheBeach' # dweet.io thing name
```

Script will put all Tag's sensors in one dweet for one Thing.

```
{
	'TAG_NAME1 temperature': VALUE,
	'TAG_NAME1 humidity': VALUE,
	'TAG_NAME1 pressure': VALUE,
	'TAG_NAME2 temperature': VALUE,
	'TAG_NAME2 humidity': VALUE,
	'TAG_NAME2 pressure': VALUE,
	etc...
}

```
If you want to save data to local database, enable it:

```python
db = True # Enable or disable database saving True/False
dbFile = '/home/pi/ruuvitag/ruuvitag.db' # path to db file
```

Script will automatically create `ruuvitag.db` file and table for sensor data.

Set execution rights to the file:

```bash
$ chmod 755 ruuvitag-logger.py
```

Now you can try to run it manually:

```bash
$ ./ruuvitag-logger.py
OR
$ /home/pi/ruuvitag/ruuvitag-logger.py
OR
$ python3 ruuvitag-logger.py
```

Set crontab to run logger automatically every 30 mins:
```bash
Add this line to the /etc/crontab file

*/30 *  * * *   pi      /home/pi/ruuvitag/ruuvitag-logger.py > /home/pi/ruuvitag/ruuvitag.log 2> /home/pi/ruuvitag/ruuvitag.err
```
Cron will output success log to `ruuvitag.log` file and errors to `ruuvitag.err` file.

## Setup web-server

Edit `ruuvitag-web.py` file.

Set charting period in days:

```python
N = 30 # show charts for 30 days
```

Set execution rights to the file:

```bash
$ chmod 755 ruuvitag-web.py
```

Now you can try to run it manually with sudo:

```bash
$ sudo ./ruuvitag-web.py
OR
$ sudo /home/pi/ruuvitag/ruuvitag-web.py
OR
$ sudo python3 ruuvitag-web.py
```

To run script in background, use nohup:

```bash
$ sudo nohup ./ruuvitag-web.py &
```

The server's output log will be in `nohup.out` file.

Server will listen requests in 80 port as normal web server do. Just open Raspberry's IP address in your browser.

To change page layout or to add more stuff, tinker with `templates/ruuvitag.html` template file.
