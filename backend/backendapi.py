from fastapi import FastAPI
from pydantic import BaseModel

from healthcareapp.main import run_agent



app = FastAPI(

    title="Healthcare AI Command Center API",

    description="Multi-Agent Healthcare Platform",

    version="1.0"

)



class ChatRequest(BaseModel):

    patient_id:str
    patient_name:str

    patient_email:str

    patient_mobile:str

    age:int

    gender:str

    query:str





@app.get("/")
def home():

    return {

        "status":"Healthcare AI API running"

    }





@app.post("/chat")
def chat(request:ChatRequest):


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
def appointment(request:ChatRequest):


    result = run_agent(

        "book doctor appointment "
        + request.query

    )


    return result





@app.post("/insurance")
def insurance(request:ChatRequest):


    result = run_agent(

        "check insurance "
        + request.query

    )


    return result