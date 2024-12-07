from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from database import init_db, save_appointment
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI()

# Initialize the database when the server starts
init_db()

# Simple state management (in-memory for simplicity)
user_states = {}

# Load templates from the 'templates' directory
templates = Jinja2Templates(directory="templates")
# Mount the 'static' directory to serve CSS files
from fastapi.staticfiles import StaticFiles
app.mount("/static", StaticFiles(directory="static"), name="static")

# Route to render the home page
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_id = data.get("user_id")
    message = data.get("message", "").lower()

    if user_id not in user_states:
        user_states[user_id] = {"step": 0}

    state = user_states[user_id]

    # Step-by-step conversation flow
    if state["step"] == 0:
        state["step"] = 1
        return JSONResponse({"response": "How can I assist you? Please tell me your problem.", "working": [1,2,3,4,45]})

    elif state["step"] == 1:
        if "fever" in message:
            state["step"] = 2
            return JSONResponse({"response": "Your symptoms match with general physicians.\nAvailable doctors: Dr. A, Dr. B, Dr. C.\nPlease choose a doctor."})
        else:
            return JSONResponse({"response": "I can only assist with fever cases currently. Please specify 'fever'."})

    elif state["step"] == 2:
        if "dr a" in message or "dr b" in message or "dr c" in message:
            state["doctor"] = message
            state["step"] = 3
            return JSONResponse({"response": f"{message.title()} is available at 10:00 PM Monday. Please confirm the time."})
        else:
            return JSONResponse({"response": "Please choose between Dr. A, Dr. B, or Dr. C."})

    elif state["step"] == 3:
        if "10:00 pm monday" in message:
            state["time"] = "10:00 PM Monday"
            state["step"] = 4
            return JSONResponse({"response": "Please provide your name."})
        else:
            return JSONResponse({"response": "Please confirm the time as '10:00 PM Monday'."})

    elif state["step"] == 4:
        state["name"] = message
        state["step"] = 5
        return JSONResponse({"response": "Please provide your phone number."})

    elif state["step"] == 5:
        state["phone"] = message
        save_appointment(state["name"], state["phone"], state["doctor"], state["time"])
        del user_states[user_id]  # Clear state after completion
        return JSONResponse({"response": f"Your appointment is confirmed with {state['doctor'].title()} at {state['time']}. Thank you!"})

    else:
        return JSONResponse({"response": "Sorry, something went wrong. Let's start over."})
