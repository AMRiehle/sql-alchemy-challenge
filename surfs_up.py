# Import dependencies

from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import pandas as pd
import numpy as np

# Connect to SQLite database

engine = create_engine("sqlite:///hawaii.sqlite")
conn = engine.connect()

# Automap classes to access data from SQLite database

Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurements
Station = Base.classes.stations

# Initiate session

session = Session(engine)

# Allow Flask to access app using file name

app = Flask(__name__)

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"<b>Available Routes:</b><br/>"
        f"<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/[start]<br/>"
        f"/api/v1.0/[end]<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation_values():
    """Return the precipitation values as json"""
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date > '2016-08-23').all()
    prcp_records = list(np.ravel(results))
    return jsonify(prcp_records)

@app.route("/api/v1.0/stations")
def station_names():
    """Return the station names as json"""
    results = session.query(Station.station).all()
    station_names = list(np.ravel(results))
    return jsonify(station_names)

@app.route("/api/v1.0/tobs")
def temp_values():
    """Return the temperature values as json"""
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date > '2016-08-23').all()
    tobs_records = list(np.ravel(results))
    return jsonify(tobs_records)

@app.route("/api/v1.0/<start>")
def temp_agr_start(start):
    """Return the aggregate temperature values with start date as json"""
    min_res = session.query(func.min(Measurement.tobs)).filter(Measurement.date >= start).first()[0]
    avg_res = session.query(func.avg(Measurement.tobs)).filter(Measurement.date >= start).first()[0]
    max_res = session.query(func.max(Measurement.tobs)).filter(Measurement.date >= start).first()[0]
    results = {'TMIN':min_res, 'TAVG':avg_res, 'TMAX':max_res}
    return jsonify(results)

@app.route("/api/v1.0/<start>/<end>")
def temp_agr_start_end(start, end):
    """Return the aggregate temperature values with start and end dates as json"""
    min_res = session.query(func.min(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).first()[0]
    avg_res = session.query(func.avg(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).first()[0]
    max_res = session.query(func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).first()[0]
    results = {'TMIN':min_res, 'TAVG':avg_res, 'TMAX':max_res}
    return jsonify(results)