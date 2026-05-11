from sqlmodel import SQLModel, Session, create_engine
import sqlite3
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine (sqlite_url, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

def get_connection():
    return sqlite3.connect("database.db")
def crear_tablas():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS operadores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        nombre_completo TEXT NOT NULL,
        hashed_password TEXT NOT NULL,
        rol TEXT NOT NULL,
        activo INTEGER NOT NULL
    )
    """)

    conn.commit()
    conn.close()

def insertar_operadores():
    conn = get_connection()
    cursor = conn.cursor()

    operadores = [
        (
            "op_martinez",
            "Laura Martinez",
            pwd_context.hash("operador123"),
            "operador",
            1
        ),
        (
            "sup_gomez",
            "Carlos Gomez",
            pwd_context.hash("supervisor456"),
            "supervisor",
            1
        ),
        (
            "op_inactivo",
            "Pedro Inactivo",
            pwd_context.hash("clave789"),
            "operador",
            0
        )
    ]

    for op in operadores:
        try:
            cursor.execute("""
            INSERT INTO operadores
            (username, nombre_completo, hashed_password, rol, activo)
            VALUES (?, ?, ?, ?, ?)
            """, op)
        except:
            pass

    conn.commit()
    conn.close()

def obtener_operador(username):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT username, nombre_completo,
           hashed_password, rol, activo
    FROM operadores
    WHERE username = ?
    """, (username,))

    resultado = cursor.fetchone()

    conn.close()

    if resultado:
        return {
            "username": resultado[0],
            "nombre_completo": resultado[1],
            "hashed_password": resultado[2],
            "rol": resultado[3],
            "activo": bool(resultado[4])
        }

    return None

def listar_operadores_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT username, nombre_completo, rol, activo
    FROM operadores
    """)

    datos = cursor.fetchall()

    conn.close()

    operadores = []

    for op in datos:
        operadores.append({
            "username": op[0],
            "nombre_completo": op[1],
            "rol": op[2],
            "activo": bool(op[3])
        })

    return operadores
