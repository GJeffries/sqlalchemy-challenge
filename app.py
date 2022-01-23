import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

###########################################################

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()

Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

##########################################################

app = Flask(__name__)

##########################################################

@app.route("/")
def home():
    return(
        f"Available Routes:<br/>"  
        f"Precipitation Route:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"Stations Route:<br/>"
        f"/api/v1.0/stations<br/>"
        f"Tobs Route:<br/>"
        f"/api/v1.0/tobs<br/>"
    )

###########################################################

@app.route('/api/v1.0/precipitation')
def precipitation():
    session = Session(engine)
    prcp_db = session.query(Measurement.date, Measurement.prcp).all()
    session.close()

    precipitation = []
    for date, prcp in prcp_db:
        prcp_data = {}
        prcp_data["Date"] = date
        prcp_data["Precipitation"] = prcp
        precipitation.append(prcp_data)

    return jsonify(precipitation)

##########################################################
   
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    station_db = session.query(Station.station, Station.name).all()
    session.close()

    stations = []
    for station,name,latitude,longitude,elevation in station_db:
        station_data = {}
        station_data["Station"] = station
        station_data["Name"] = name
        station_data["Lat"] = latitude
        station_data["Lon"] = longitude
        station_data["Elevation"] = elevation
        stations.append(station_data)
    
    # jsonify the list
    return jsonify(stations)

############################################################

@app.route('/api/v1.0/tobs')
def tobs():
    session = Session(engine)
    tobs_db = session.query(Measurement.tobs, Measurement.date).filter(Measurement.date >= query_date).all()
    session.close()

    tobs_list = []
    for date, tobs in tobs_db:
        tobs_data = {}
        tobs_data["Date"] = date
        tobs_data["Tobs"] = tobs
        tobs_list.append(tobs_data)

    return jsonify(tobs_list)

############################################################

if __name__ == "__main__":
    app.run(debug=True)