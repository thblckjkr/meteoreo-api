from fastapi import FastAPI
from models import Station
from schemas import StationSchema
import os

app = FastAPI()

@app.get("/stations")
def read_stations():
	stations = Station.all()
	return { "stations": stations }

@app.put("/stations")
def put_station( station: StationSchema.Schema ):
	"""
	Create a station with all the information:
	"""
	result = Station.create(
		{
			'name': name,
			'ip': ip
		}
	)
	return {"result": result}

@app.get("/stations/{station_uuid}")
def read_item(station_uuid: str = None):
	return {"item_id": item_id, "q": q}
