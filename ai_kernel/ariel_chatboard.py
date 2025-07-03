import os
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from starlette.templating import Jinja2Templates

CHAT_PASSWORD = "changeme"  # CHANGE THIS!

ENABLE_KILL_SWITCH = True

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="supersecretkey123")
base_dir = os.path.abspath(os.path.dirname(__file__))
templates = Jinja2Templates(directory=os.path.join(base_dir, "templates"))
app.mount("/static", StaticFiles(directory=os.path.join(base_dir, "static")), name="static")

@app.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "error": ""})

@app.post("/login", response_class=HTMLResponse)
async def login_post(request: Request, password: str = Form(...)):
    if password == CHAT_PASSWORD:
        request.session["logged_in"] = True
        return RedirectResponse(url="/", status_code=302)
    else:
        return templates.TemplateResponse("login.html", {"request": request, "error": "Incorrect password."})

@app.get("/logout", response_class=HTMLResponse)
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/login", status_code=302)

def require_login(func):
    async def wrapper(request: Request, *args, **kwargs):
        if not request.session.get("logged_in"):
            return RedirectResponse(url="/login", status_code=302)
        return await func(request, *args, **kwargs)
    return wrapper

@app.get("/", response_class=HTMLResponse)
@require_login
async def chat_board(request: Request):
    chat_history = request.session.get("chat_history", [])
    return templates.TemplateResponse("dashboard.html", {"request": request, "chat_history": chat_history})

@app.post("/chat", response_class=HTMLResponse)
@require_login
async def chat(request: Request, user_input: str = Form(...)):
    chat_history = request.session.get("chat_history", [])
    chat_history.append({"role": "user", "text": user_input})
    ariel_response = f"Ariel: I received '{user_input}'."
    chat_history.append({"role": "ariel", "text": ariel_response})
    request.session["chat_history"] = chat_history
    return templates.TemplateResponse("dashboard.html", {"request": request, "chat_history": chat_history})

@app.post("/clear", response_class=HTMLResponse)
@require_login
async def clear_chat(request: Request):
    request.session["chat_history"] = []
    return RedirectResponse(url="/", status_code=302)

if ENABLE_KILL_SWITCH:
    @app.post("/kill", response_class=HTMLResponse)
    @require_login
    async def kill(request: Request):
        open(os.path.join(base_dir, "KILL_ARIEL"), "w").close()
        return HTMLResponse("Kill switch activated. Please restart the system for changes to take effect.")
