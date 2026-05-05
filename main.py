from fastapi import FastAPI
from api.database import create_db_and_tables
from api.routers.usuarios import router as router_usuarios
from api.routers.permisos import router as router_permisos 
from api.routers.roles import router as router_roles
from api.routers.vehiculos import router as router_vehiculos



app = FastAPI(title="CargoTrack API")

@app.event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(router_usuarios)
app.include_router(router_permisos)
app.include_router(router_roles)
app.include_router(router_vehiculos)


