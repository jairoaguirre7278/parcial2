from fastapi import APIRouter

router = APIRouter(prefix= "/api/vehiculos")

@router.get("/vehiculos")
def read_root(
):
    pass


@router.get("/vehiculos/{id}")
def read_root(
):
   pass


@router.post("/vehiculos")
def crear_estudiante():
    pass