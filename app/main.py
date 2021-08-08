from fastapi import Depends, FastAPI
from dotenv import load_dotenv
import os

from app.routers import stations

# Load environment variables (from .env) and add them to the os.getenv() function
load_dotenv()

description = """
Meteoreo API

Meteoreo is a system for monitoring and control oriented to meteorological stations. This API is one of the three main components of the system. This API permits you to modify and create the data required for a meteorological station, and to obtain the global status of them. *Así como* send (directly, or in a queue) a system command to the station, if available.

Meteoreo es un sistema de monitoreo y control orientado a estaciones meteorológicas, el API es uno de los tres componentes principales del sistema. Este permite agregar y modificar los datos de las estaciones que se monitorean, así com obtener el estatus general de las mismas y enviar comandos directamente, así como enviar un comando en método pull.
"""

app = FastAPI(
	title="Meteoreo API",
	description=description,
	version=os.getenv("VERSION"),
	contact={
		"name": "Teo González Calzada",
		"url": "https://thblckjkr.tk",
		"email": "teo@thblckjkr.tk"
	},
	license_info={
		"name": "GNU v3",
		"url": "https://www.gnu.org/licenses/gpl-3.0.html"
	},
	docs_url="/docs_legacy",
	redoc_url="/docs"
)

app.include_router(stations.router)
