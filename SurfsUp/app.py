# Import the dependencies.
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine('sqlite:///Resources/hawaii.sqlite')

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

end_date = session.query(measurement.date).order_by(measurement.date.desc()).first()[0]
end_date = dt.datetime.strptime(end_date, "%Y-%m-%d")
start_date = end_date - dt.timedelta(days=365)

@app.route("/")
def homepage():
    """List all available api routes."""
    return (
        f"<h1>Available Routes:<br/></h1>"
        f"<br>"
        f"<b>/api/v1.0/precipitation</b> -- Precipitation data for the past year<br/>"
        f"<br>"
        f"<b>/api/v1.0/stations</b> -- List of station call-numbers and names<br/>"
        f"<br>"
        f"<b>/api/v1.0/tobs</b> -- Temperature observations from our most active station from the past year<br/>"
        f"<br>"
        f"<b>api/v1.0/temp_desc/start=<i>(enter date in YYYY-MM-DD format)</i></b> -- Temperature observations from a specific start date to the most recent observation data<br/>"
        f"<br>"
        f"<b>/api/v1.0/temp_desc/start=<i>(enter date in YYYY-MM-DD format)</i>/end=<i>(enter date in YYYY-MM-DD format)</i></b> -- Temperature observations from a specific start date to a specific end date<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    # Gather all data from past year (date and prcp info)
    precip = session.query(measurement.date, measurement.prcp).\
        filter(measurement.date >= start_date).order_by(measurement.date).all()

    session.close()

    # Convert to dictionary for JSON
    results_list = []
    for date, prcp in precip:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["precipitation"] = prcp
        results_list.append(prcp_dict)
    return jsonify(results_list)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Create list of all stations to be jsonified
    stations = {}

    station_query = session.query(station.station, station.name).all()
    for station_code, name in station_query:
        stations[station_code] = name
    session.close()

    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Gather tobs info for past year from most active station
    tobs_query = session.query(measurement.date, measurement.tobs).\
        filter(measurement.station == "USC00519281").\
        filter(measurement.date >= start_date).all()
    
    session.close()

    # Convert to dictionary for JSON
    tobs_list = []
    for date, tobs in tobs_query:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        tobs_list.append(tobs_dict)

    return jsonify(tobs_list)

@app.route("/api/v1.0/temp_desc/start=<start>")
def start_only(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Gather min, avg, and max data from a specified date to end of dataset
    start_desc = session.query(func.min(measurement.tobs),\
                                func.avg(measurement.tobs),\
                                func.max(measurement.tobs)).\
                                filter(measurement.date >= start).all()
    session.close()

    # Convert to dictionary for JSON
    start_list = []
    for min, avg, max in start_desc:
        desc_dict = {}
        desc_dict["TMIN"] = min
        desc_dict["TAVG"] = avg
        desc_dict["TMAX"] = max
        start_list.append(desc_dict)

    return jsonify(start_list)

@app.route("/api/v1.0/temp_desc/start=<start>/end=<end>")
def start_end(start, end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Gather min, avg, and max data between two specified dates
    start_end_desc = session.query(func.min(measurement.tobs),\
                                func.avg(measurement.tobs),\
                                func.max(measurement.tobs)).\
                                filter(measurement.date >= start).\
                                filter(measurement.date <= end).all()
    session.close()

    # Convert to dictionary for JSON
    start_end_list = []
    for min, avg, max in start_end_desc:
        end_desc_dict = {}
        end_desc_dict["TMIN"] = min
        end_desc_dict["TAVG"] = avg
        end_desc_dict["TMAX"] = max
        start_end_list.append(end_desc_dict)

    return jsonify(start_end_list)

if __name__ == "__main__":
    app.run(debug=True)