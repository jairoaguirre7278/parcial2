from fastapi import APIRouter

router = APIRouter(prefix= "/api/usuarios")

@router.get("/usuarios")
def read_root(
):
    pass


@router.get("/usuarios/{id}")
def read_root(
):
   pass


@router.post("/usuarios")
def crear_estudiante():
    pass