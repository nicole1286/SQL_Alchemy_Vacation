import numpy as np 
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# 2. Create an app, being sure to pass __name__
app = Flask(__name__)
session = Session(engine)
# 3. Define what to do when a user hits the index route
@app.route("/")
def home():
    return(
        f"Available Routes:<br>"
        f"/api/v1.0/precipitation<br>"
        f"/api/v1.0/stations<br>"
        f"/api/v1.0/tobs<br>"
        f"/api/v1.0/<start> and /api/v1.0/<start>/<end>"
    )
@app.route("/api/v1.0/precipitation")
def precipitation():
    results = session.query(Measurement.date, Measurement.prcp).all()
    precip_all = []
    for date, prcp in results:
        precip_dict = {}
        precip_dict["date"] = date
        precip_dict["prcp"] = prcp
        precip_all.append(precip_dict)
    return jsonify(precip_all)

@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.name).all()
    station_list = []
    for name in results:
        station_dict = {}
        station_dict["name"] = name
        station_list.append(station_dict)
    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    results = session.query(Measurement.date, Measurement.tobs).all()
    temp_list = []
    for tobs in results:
        temp_dict = {}
        temp_dict["tobs"] = tobs
        temp_list.append(temp_dict)
    return jsonify(temp_list)

@app.route("/api/v1.0/<start_date>/<end_date>")
def calc_temps(start_date, end_date):
# start_date = '2017-08-10'
# end_date = '2017-08-20'
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs),\
        func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).\
        filter(Measurement.date <= end_date).all()
    return jsonify(results)
    # for tobs in results:
    #     trip_temp = []
    #     trip_temp.append
    # return(results)
    # 4. Define main behavior
if __name__ == "__main__":
    app.run(debug=True)
