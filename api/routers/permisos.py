from fastapi import APIRouter

router = APIRouter(prefix= "/api/permisos")

@router.get("/permisos")
def read_root(
):
    pass


@router.get("/permisos/{id}")
def read_root(
):
   pass


@router.post("/permisos")
def crear_estudiante():
    pass