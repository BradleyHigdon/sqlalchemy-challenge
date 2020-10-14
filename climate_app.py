%matplotlib inline
from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt

import pandas as pd
import datetime as dt
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#Creating engine
engine = create_engine("sqlite:///Resources/hawaii.sqlite", echo = False)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect = True)

# We can view all of the classes that automap found
Base.classes.keys()

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#Create app
app = Flask(__name__)

#Main route
@app.route("/")
def main():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

#Precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    
    print("API request for precipitation received")
    
    precipitation_results = session.query(Measurement.date, Measurement.prcp).\
                   filter(Measurement.date.between('2016-08-23', '2017-8-23')).all()

    precipitation = []
    for result in prcp_results:
        row = {"date":"prcp"}
        row["date"] = result[0]
        row["prcp"] = float(result[1])
        
        precipitation.append(row)

    return jsonify(precipitation)

#Stations route
@app.route("/api/v1.0/stations")
def stations():
    
    print("API request for stations received")

    stations = session.query(Station).all()

    stations_list = []
    for station in stations:
        station_dictionary = {}
        station_dictionary["id"] = station.id
        station_dictionary["station"] = station.station
        station_dictionary["name"] = station.name
        station_dictionary["latitude"] = station.latitude
        station_dictionary["longitude"] = station.longitude
        station_dictionary["elevation"] = station.elevation
        
        stations_list.append(station_dictionary)

    return jsonify(stations_list)

#Tobs route
@app.route("/api/v1.0/tobs")
def tobs():
    
    print("API tobs request received")
    
    tobs_results = session.query(Measurement.station, Measurement.tobs).filter(Measurement.date.between('2016-08-23', '2017-08-23')).all()
    
    tobs_list = []
    for tobs in tobs_results:
        tobs_dictionary = {}
        tobs_dictionary["station"] = tobs[0]
        tobs_dictionary["tobs"] = float(tobs[1])
       
        tobs_list.append(tobs_dictionary)
        
    return jsonify(tobs_list)

def calculate_temperatures(start_date, end_date):
    """TMIN, TAVG, and TMAX give a list of dates.
    
    Arg:
        start_date (string): Date string %y-%m-%d format
        end_date (string): Date string %y-%m-%d format
        
    Return: TMIN, TAVG, TMAX"""
    
    
    return session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

#Start route
@app.route("/api/v1.0/<start>")
def start(start):

    print("API request for start date received")

    last_date_query = session.query(func.max(func.strftime("%y-%m-%d", Measurement.date.between('2016-08-23', '2017-08-23')))).all()
    max_date = last_date_query[0][0]

    temperatures = calculate_temperatures(start, max_date)

    return_list = []
    date_dict = {'start_date': start, 'end_date': max_date}
    return_list.append(date_dict)
    return_list.append({'Observation': 'TMIN', 'Temperature': temperatures[0][0]})
    return_list.append({'Observation': 'TAVG', 'Temperature': temperatures[0][1]})
    return_list.append({'Observation': 'TMAX', 'Temperature': temperatures[0][2]})

    return jsonify(return_list)

#Start route
@app.route("/api/v1.0/<start>")
def start(start):

    print("API request for start date received")

    last_date_query = session.query(func.max(func.strftime("%y-%m-%d", Measurement.date.between('2016-08-23', '2017-08-23')))).all()
    max_date = last_date_query[0][0]

    temperatures = calculate_temperatures(start, max_date)

    return_list = []
    date_dict = {'start_date': start, 'end_date': max_date}
    return_list.append(date_dict)
    return_list.append({'Observation': 'TMIN', 'Temperature': temperatures[0][0]})
    return_list.append({'Observation': 'TAVG', 'Temperature': temperatures[0][1]})
    return_list.append({'Observation': 'TMAX', 'Temperature': temperatures[0][2]})

    return jsonify(return_list)

if __name__ == "__main__":
    app.run(debug = True)