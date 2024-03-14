from fastapi import FastAPI, HTTPException

app = FastAPI(
    title="Gestión de Usuarios",
    version="1.0.0"
)

# Almacenamiento temporal de usuarios registrados (simulación)
registered_users = {}

class User:
    def __init__(self, username: str, email: str, password: str):
        self.username = username
        self.email = email
        self.password = password

@app.post("/register")
async def register_user(username: str, email: str, password: str):
    if username in registered_users:
        raise HTTPException(status_code=400, detail="El usuario ya está registrado")

    # Almacenar el usuario registrado
    user = User(username=username, email=email, password=password)
    registered_users[username] = user
    return {"message": "Usuario registrado exitosamente"}

# API para obtener datos de usuario por ID
@app.get("/user/{id}")
async def get_user_by_id(id: str):
    user = registered_users.get(id)
    if not user:
        raise HTTPException(status_code=404, detail="El usuario no existe")
    return user.__dict__