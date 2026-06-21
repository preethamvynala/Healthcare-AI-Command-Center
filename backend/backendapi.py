from fastapi import FastAPI
from pydantic import BaseModel

from fastapi.middleware.cors import CORSMiddleware



app = FastAPI(

    title="Healthcare AI Command Center API",

    description="Multi-Agent Healthcare Platform",

    version="1.0"

)



# =====================================
# CORS Configuration
# =====================================

app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],

)



# =====================================
# Lazy Load LangGraph Agent
# Reduces Render RAM usage
# =====================================

def get_agent():

    from healthcareapp.main import run_agent

    return run_agent




# =====================================
# Request Model
# =====================================

class ChatRequest(BaseModel):

    patient_id: str

    patient_name: str

    patient_email: str

    patient_mobile: str

    age: int

    gender: str

    query: str




# =====================================
# Health Check
# =====================================

@app.get("/")
def home():

    return {

        "status":
        "Healthcare AI API running"

    }





# =====================================
# Main Chat Endpoint
# =====================================

@app.post("/chat")
def chat(request: ChatRequest):


    run_agent = get_agent()


    result = run_agent(

        question=request.query,

        patient_id=request.patient_id,

        patient_name=request.patient_name,

        patient_email=request.patient_email,

        patient_mobile=request.patient_mobile,

        age=request.age,

        gender=request.gender

    )


    return result





# =====================================
# Appointment Endpoint
# =====================================

@app.post("/appointment")
def appointment(request: ChatRequest):


    run_agent = get_agent()



    result = run_agent(

        question=
        "book doctor appointment "
        + request.query,


        patient_id=request.patient_id,

        patient_name=request.patient_name,

        patient_email=request.patient_email,

        patient_mobile=request.patient_mobile,

        age=request.age,

        gender=request.gender

    )


    return result





# =====================================
# Insurance Endpoint
# =====================================

@app.post("/insurance")
def insurance(request: ChatRequest):


    run_agent = get_agent()



    result = run_agent(

        question=
        "check insurance "
        + request.query,


        patient_id=request.patient_id,

        patient_name=request.patient_name,

        patient_email=request.patient_email,

        patient_mobile=request.patient_mobile,

        age=request.age,

        gender=request.gender

    )


    return result