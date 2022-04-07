import os

from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

from app.routers import stations
from app.routers import drivers
from app.routers import incidents
from app.routers import authentication

# Load environment variables (from .env) and add them to the os.getenv() function
load_dotenv()

# Define valid origin for CORS
origins = [
    "http://127.0.0.1:8080",
    "https://cecatev.uacj.mx",
    "http://cecatev.uacj.mx",
    "http://localhost:8080",
]

DESCRIPTION = """
Meteoreo API

Meteoreo is a system for monitoring and control oriented to meteorological stations. This API is one of the three main components of the system. This API permits you to modify and create the data required for a meteorological station, and to obtain the global status of them. *Así como* send (directly, or in a queue) a system command to the station, if available.

Meteoreo es un sistema de monitoreo y control orientado a estaciones meteorológicas, el API es uno de los tres componentes principales del sistema. Este permite agregar y modificar los datos de las estaciones que se monitorean, así com obtener el estatus general de las mismas y enviar comandos directamente, así como enviar un comando en método pull.
"""

app = FastAPI(
    title="Meteoreo API",
    description=DESCRIPTION,
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
    redoc_url="/api/v1/docs",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(stations.router, prefix="/api/v1")
app.include_router(drivers.router, prefix="/api/v1")
app.include_router(incidents.router, prefix="/api/v1")
app.include_router(authentication.router, prefix="/api/v1")
