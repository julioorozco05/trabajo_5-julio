from enum import Enum
from fastapi import FastAPI, HTTPException

app = FastAPI(
    title="Gestión de Usuarios",
    version="1.0.0"
)

# Almacenamiento temporal de usuarios registrados (simulación)
registered_users = {}
user_tasks = {}

class User:
    def __init__(self, username: str, email: str, password: str):
        self.username = username
        self.email = email
        self.password = password

class TaskStatus(str, Enum):
    PENDIENTE = "pendiente"
    EN_PROGRESO = "en progreso"
    COMPLETADA = "completada"

class Task:
    def __init__(self, title: str, description: str, status: TaskStatus):
        self.title = title
        self.description = description
        self.status = status


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

@app.post("/task/create")
async def create_task(user_id: str, title: str, description: str, status: TaskStatus):
    if user_id not in registered_users:
        raise HTTPException(status_code=404, detail="El usuario no existe")

    task = Task(title=title, description=description, status=status)

    if user_id not in user_tasks:
        user_tasks[user_id] = []
    user_tasks[user_id].append(task)

    return {"message": "Tarea creada exitosamente"}

# API para obtener todas las tareas de un usuario
@app.get("/tasks/{user_id}")
async def get_user_tasks(user_id: str):
    # Verificar si el usuario existe
    if user_id not in registered_users:
        raise HTTPException(status_code=404, detail="El usuario no existe")

    # Obtener las tareas asociadas al usuario
    tasks = user_tasks.get(user_id, [])
    if not tasks:
        return {"message": "El usuario no tiene tareas"}

    return tasks
