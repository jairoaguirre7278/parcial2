from fastapi import APIRouter

router = APIRouter(prefix= "/api/roles")

@router.get("/roles")
def read_root(
):
    pass



@router.post("/roles")
def crear_estudiante():
    pass