from fastapi import FastAPI
from models import Station
from schemas import StationSchema
import os

from pydantic import BaseModel

app = FastAPI()

@app.get("/stations")
def read_stations():
	stations = Station.all()
	return { "stations": stations }

@app.put("/stations")
def put_station( station: StationSchema.Schema ):
	"""
    Create an item with all the information:

    - **name**: each item must have a name
    - **description**: a long description
    - **price**: required
    - **tax**: if the item doesn't have tax, you can omit this
    - **tags**: a set of unique tag strings for this item
    \f
    :param item: User input.
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
