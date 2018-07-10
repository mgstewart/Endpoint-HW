# Import dependencies
from datetime import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# Create the engine object for our hawaii.sqlite
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a Base class
Base = automap_base()
# reflect the tables into the delcarative base
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurements = Base.classes.measurements
Stations = Base.classes.stations

# Create our session (link) from Python to the DB
session = Session(engine)

# Set up Flask
app = Flask(__name__)

# Set up Flask Routes
# Set up the root route to display other options
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/YYYY-MM-DD<br/>"
        f"/api/v1.0/temp/YYYY-MM-DD/YYYY-MM-DD<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Declare an empty dictionary which will hold date: tobs pairs
    climate_dict = {}
    start_date = '2016-08-23'
    end_date = '2017-08-23'
    # Construct query object to pull tobs data
    q = session.query(Measurements.station,Measurements.date,Measurements.tobs).\
        filter(Measurements.date >= start_date,Measurements.date <= end_date).\
        order_by(Measurements.date)
    #print(f"The provided query is: {q}")
    r = q.all()
    # Loop over the results and pull the dates and prcp data into lists for a df
    for result in r:
        _datestring = dt.strftime(result[1],'%Y-%m-%d')
        climate_dict[_datestring] = result[2]
    return jsonify(climate_dict)

@app.route("/api/v1.0/stations")
def stations():
    # Declare an empty list to hold station names
    list_of_stations = []
    # Query the Station ID's from the stations table
    # Personally, I think it'd be more meaningful to return the table
    # as a JSONified dictionary, but that's just me spitballin'
    q = session.query(Stations.station,Stations.name)
    r = q.all()
    for result in r:
        list_of_stations.append(result[0])
    return jsonify(list_of_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Declare an empty list of tobs to fill with queried values
    list_of_tobs = []
    start_date = '2016-08-23'
    end_date = '2017-08-23'
    # Construct query object to pull tobs data
    q = session.query(Measurements.station,Measurements.date,Measurements.tobs).\
        filter(Measurements.date >= start_date,Measurements.date <= end_date).\
        order_by(Measurements.date)
    #print(f"The provided query is: {q}")
    r = q.all()
    # Loop over the results and pull the dates and prcp data into lists for a df
    for result in r:
        list_of_tobs.append(result[2])
    return jsonify(list_of_tobs)

@app.route("/api/v1.0/temp/<start>")
def temp_analysis(start):
    list_of_temps = []
    output_list = []
    start_date = start
    # Construct query object to pull tobs data
    q = session.query(Measurements.station,Measurements.date,Measurements.tobs).\
        filter(Measurements.date >= start_date).\
        order_by(Measurements.date)
    r = q.all()
    # Loop over the results and pull the tobs data into a list
    for result in r:
        list_of_temps.append(result[2])
    # Use NumPy to find the mean, max, and average values and store in a new list
    output_list.append(int(np.min(list_of_temps)))
    output_list.append(int(np.mean(list_of_temps)))
    output_list.append(int(np.max(list_of_temps)))
    return jsonify(output_list)

@app.route("/api/v1.0/temp/<start>/<end>")
def temp_analysis_2(start,end):
    list_of_temps = []
    output_list = []
    start_date = start
    end_date = end
    # Construct query object to pull tobs data
    q = session.query(Measurements.station,Measurements.date,Measurements.tobs).\
        filter(Measurements.date >= start_date,Measurements.date <= end_date).\
        order_by(Measurements.date)
    r = q.all()
    # Loop over the results and pull the tobs data into a list
    for result in r:
        list_of_temps.append(result[2])
    # Use NumPy to find the mean, max, and average values and store in a new list
    output_list.append(int(np.min(list_of_temps)))
    output_list.append(int(np.mean(list_of_temps)))
    output_list.append(int(np.max(list_of_temps)))
    return jsonify(output_list)

if __name__ == '__main__':
    app.run(debug=True)