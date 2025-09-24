from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI, WebSocket
from routers import auth, projects, tasks
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

@app.websocket("/ws/tasks/{project_id}")
async def websocket_endpoint(websocket: WebSocket, project_id: int):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message received for project {project_id}: {data}")

app.include_router(auth.router)
app.include_router(projects.router)
app.include_router(tasks.router)

