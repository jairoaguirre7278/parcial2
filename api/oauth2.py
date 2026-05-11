from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from datetime import datetime, timedelta
from typing import Optional

from .database import obtener_operador

SECRET_KEY = "cargotrack-clave-secreta-no-usar-en-produccion"
ALGORITHM = "HS256"
EXPIRACION_MINUTOS = 30

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class Operador(BaseModel):
    username: str
    nombre_completo: str
    rol: str
    activo: bool

def verificar_contrasena(plana: str, hasheada: str):
    return pwd_context.verify(plana, hasheada)

def crear_token(datos: dict, delta: Optional[timedelta] = None):

    datos_copia = datos.copy()

    if delta:
        expiracion = datetime.utcnow() + delta
    else:
        expiracion = datetime.utcnow() + timedelta(minutes=15)

    datos_copia.update({"exp": expiracion})

    return jwt.encode(
        datos_copia,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

async def obtener_operador_actual(
    token: str = Depends(oauth2_scheme)
):

    excepcion = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token invalido o expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        username = payload.get("sub")

        if username is None:
            raise excepcion

    except JWTError:
        raise excepcion

    datos_op = obtener_operador(username)

    if datos_op is None:
        raise excepcion

    if not datos_op["activo"]:
        raise HTTPException(
            status_code=400,
            detail="Operador inactivo"
        )

    return Operador(
        username=datos_op["username"],
        nombre_completo=datos_op["nombre_completo"],
        rol=datos_op["rol"],
        activo=datos_op["activo"]
    )
