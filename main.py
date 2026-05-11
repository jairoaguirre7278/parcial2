from fastapi import FastAPI
from api.database import create_db_and_tables
from api.routers.usuarios import router as router_usuarios
from api.routers.permisos import router as router_permisos 
from api.routers.roles import router as router_roles
from api.routers.vehiculos import router as router_vehiculos
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

from api.oauth2 import (
    verificar_contrasena,
    crear_token,
    obtener_operador_actual,
    Operador,
    EXPIRACION_MINUTOS
)

from api.database import (
    crear_tablas,
    insertar_operadores,
    obtener_operador,
    listar_operadores_db
)

app = FastAPI(title="CargoTrack API")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    crear_tablas()
    insertar_operadores()

@app.post("/token")
async def login(
    form: OAuth2PasswordRequestForm = Depends()
):

    datos_op = obtener_operador(form.username)

    if not datos_op:
        raise HTTPException(
            status_code=401,
            detail="Usuario no encontrado"
        )

    if not verificar_contrasena(
        form.password,
        datos_op["hashed_password"]
    ):
        raise HTTPException(
            status_code=401,
            detail="Contraseña incorrecta"
        )

    if not datos_op["activo"]:
        raise HTTPException(
            status_code=400,
            detail="Operador inactivo"
        )

    token = crear_token(
        datos={
            "sub": datos_op["username"],
            "rol": datos_op["rol"]
        },
        delta=timedelta(minutes=EXPIRACION_MINUTOS)
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }

@app.get("/operador/perfil")
async def mi_perfil(
    operador: Operador = Depends(obtener_operador_actual)
):

    return operador

@app.get("/envios/activos")
async def envios(
    operador: Operador = Depends(obtener_operador_actual)
):

    return {
        "usuario": operador.username,
        "envios": [
            {
                "id": "ENV-001",
                "destino": "Bogota",
                "estado": "En transito"
            },
            {
                "id": "ENV-002",
                "destino": "Cali",
                "estado": "Pendiente"
            }
        ]
    }

@app.delete("/envios/{envio_id}")
async def cancelar_envio(
    envio_id: str,
    operador: Operador = Depends(obtener_operador_actual)
):

    if operador.rol != "supervisor":
        raise HTTPException(
            status_code=403,
            detail="Solo supervisores pueden cancelar"
        )

    return {
        "mensaje": f"Envio {envio_id} cancelado",
        "cancelado_por": operador.username
    }

@app.get("/admin/operadores")
async def listar_operadores(
    operador: Operador = Depends(obtener_operador_actual)
):

    if operador.rol != "supervisor":
        raise HTTPException(
            status_code=403,
            detail="Solo supervisores pueden acceder"
        )        fastapi dev main.py

    return listar_operadores_db()


app.include_router(router_usuarios)
app.include_router(router_permisos)
app.include_router(router_roles)
app.include_router(router_vehiculos)



