from fastapi import FastAPI
from fastapi.responses import JSONResponse
import subprocess
import time

app = FastAPI()
ariel_status = {
    "running": True,
    "last_active": time.time(),
    "errors": 0,
    "message": "Ariel is alive!"
}

@app.get("/ariel/status")
def get_status():
    return ariel_status

@app.get("/ariel/logs")
def get_logs():
    try:
        logs = subprocess.check_output(["tail", "-n", "40", "ariel.log"]).decode()
    except Exception:
        logs = "No logs found."
    return JSONResponse(content={"logs": logs})

@app.post("/ariel/pause")
def pause():
    ariel_status["running"] = False
    ariel_status["message"] = "Ariel is paused!"
    return ariel_status

@app.post("/ariel/resume")
def resume():
    ariel_status["running"] = True
    ariel_status["message"] = "Ariel is running!"
    return ariel_status
