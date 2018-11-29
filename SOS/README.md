# SOS Working

Some documentation about feeding SOS database with data from MONALISA project.

We distinguish between two main sections:

* Sensors
* Observations

## Sensors 
If you want to insert data to SOS database, you first need to insert the sensor
where the data was taken from. It is used to describe the type of the measurements
and all observed parameters.

Take a look at the GitLab repository, where you can find all Insert_Sensor xml
files: [Sensors](https://github.com/danji90/Personal_GitHub/tree/master/SOS/monalisa_sos/Insert_Sensor)

## Observations
The data input files are heterogenous and need different scripts to upload them
into the database. There are different station types:

* Orchard
* Grassland (Standard, Standard+SRS)
* Beratungsring
* Meteorological stations of province Bz
* Eddy Covariance 

The raw input files for the different station categories have different formats or structure (date/time format, measured parameters, number of columns, units etc.). 
Therefore the [scripts](https://github.com/danji90/Personal_GitHub/tree/master/SOS/monalisa_sos/SCRIPT_monalisa_sos) for importing data have
to be adjusted accordingly and [templates](https://github.com/danji90/Personal_GitHub/tree/master/SOS/monalisa_sos/Templates) for inserting observations
into different stations have to be created. Since the Beratungsring script turns out to be the most effective, new input data have to have the structure and format
of Beratungsring data and the scripts must be based on the [offSOS_importdata_beratungsring.py](https://github.com/danji90/Personal_GitHub/blob/master/SOS/monalisa_sos/SCRIPT_monalisa_sos/Beratungsring/offSOS_importdata_beratungsring.py).
