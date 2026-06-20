from fastapi import FastAPI
from pydantic import BaseModel

from healthcareapp.main import run_agent

from fastapi.middleware.cors import CORSMiddleware



app = FastAPI(

    title="Healthcare AI Command Center API",

    description="Multi-Agent Healthcare Platform",

    version="1.0"

)



# =====================================
# CORS Configuration
# Allow Streamlit Frontend to call API
# =====================================

app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],

)





class ChatRequest(BaseModel):

    patient_id: str

    patient_name: str

    patient_email: str

    patient_mobile: str

    age: int

    gender: str

    query: str





@app.get("/")
def home():

    return {

        "status":
        "Healthcare AI API running"

    }





@app.post("/chat")
def chat(request: ChatRequest):


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





@app.post("/appointment")
def appointment(request: ChatRequest):


    result = run_agent(

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





@app.post("/insurance")
def insurance(request: ChatRequest):


    result = run_agent(

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