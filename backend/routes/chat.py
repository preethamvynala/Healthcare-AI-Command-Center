from fastapi import APIRouter
from pydantic import BaseModel


from healthcareapp.workflows.graph import healthcare_graph



router = APIRouter()



class ChatRequest(BaseModel):

    patient_id: str = "P001"

    query: str



@router.post("/chat")
def chat(request: ChatRequest):


    initial_state = {


        "patient_id": request.patient_id,

        "query": request.query,

        "department": None,

        "specialist": None,

        "appointment": None,

        "insurance_status": None,

        "medicine": None,

        "billing": None,

        "hospital_operations": None,

        "response": None,

        "next_agent": None,

        "approval_required": False,

        "approved": False

    }



    result = healthcare_graph.invoke(
        initial_state
    )



    return {


        "answer": result["response"],

        "state": result

    }