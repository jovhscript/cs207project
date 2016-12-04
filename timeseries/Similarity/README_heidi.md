# Initial Work

*** FILES TO USE ***
- server.py
- client_indatabase.py
- client_json.py
- tstojson.py

+ DATA FILE:
- GeneratedTimeseries/
- Timeseries0.json

*** HOW TO ***
- Run in one terminal window the server.py
- Run in a second window one of the client_xx.py:
	- This file will ask you for the Timeseries of interest and the number N of neighbours wanted.
	- Must enter in the following format:
		- if indatabase: TimeseriesXX/N
		- if json: TimeseriesXX.json/N (I've added one timeseries in json format in the directory, you can check that the results for the json and indata correspond)

*** tstojson ***

In order to transfer the timeseries in the json format, I had to add a __json__ method to the ArrayTimeSeries interface (so dont forget to pull the dev branch) as well as create encoding and decoding functions contained in tstojson.py. The sencode and sdecode methods, transform a json object into a string which we can then encode in byte and transfer to the server. 

Let me know if you need help !

