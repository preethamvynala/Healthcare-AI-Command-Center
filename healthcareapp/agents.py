from healthcareapp.llm_factory import get_llm
from healthcareapp.guardrails import validate_response
print("LOADED AGENTS FILE")
print(__file__)
import os

from dotenv import load_dotenv


BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

load_dotenv(
    os.path.join(BASE_DIR, ".env")
)


from healthcareapp.tools import (
    book_doctor,
    check_medicine,
    check_insurance,
    create_claim,
    generate_invoice,
    trigger_n8n
)


from healthcareapp.rag import search_knowledge



# ==================================================
# Lazy Loaded LLM
# Prevent Render RAM issues
# ==================================================

_llm = None


def get_agent_llm():

    global _llm


    if _llm is None:

        _llm = get_llm()


    return _llm



# ==================================================
# Agent 1
# Patient Care Coordinator Agent
# ==================================================

def patient_care_coordinator_agent(state):


    query = state["query"].lower()


    clinical_keywords = [

        "appointment",
        "doctor",
        "specialist",
        "problem",
        "issue",
        "symptom",
        "pain",
        "ache",
        "fever",
        "cough",
        "headache",
        "chest",
        "heart",
        "digestive",
        "digestion",
        "stomach",
        "gastric",
        "skin",
        "rash",
        "seizure",
        "brain",
        "bone",
        "joint",
        "ear",
        "nose",
        "throat"

    ]


    if any(word in query for word in clinical_keywords):

        state["next_agent"] = "clinical"


    elif any(word in query for word in [
        "medicine",
        "tablet",
        "drug",
        "pharmacy"
    ]):

        state["next_agent"] = "pharmacy"


    elif any(word in query for word in [
        "insurance",
        "claim"
    ]):

        state["next_agent"] = "insurance"


    elif any(word in query for word in [
        "bill",
        "invoice",
        "payment"
    ]):

        state["next_agent"] = "billing"


    else:

        state["next_agent"] = "medical_knowledge"


    return state

# ==================================================
# Agent 2
# Dynamic Specialist Router Agent
# ==================================================

def specialist_router_agent(state):


    query = state["query"].lower()


    specialist = "General Physician"



    if any(word in query for word in [
        "chest pain",
        "heart",
        "cardiac",
        "palpitation",
        "blood pressure",
        "heartbeat"
    ]):

        specialist = "Cardiologist"



    elif any(word in query for word in [
        "skin",
        "rash",
        "itching",
        "acne",
        "dermatitis",
        "pimples"
    ]):

        specialist = "Dermatologist"



    elif any(word in query for word in [
        "headache",
        "brain",
        "seizure",
        "migraine",
        "memory"
    ]):

        specialist = "Neurologist"



    elif any(word in query for word in [
        "bone",
        "joint",
        "fracture",
        "back pain"
    ]):

        specialist = "Orthopedic"



    elif any(word in query for word in [
        "ear",
        "nose",
        "throat",
        "sinus"
    ]):

        specialist = "ENT Specialist"



    elif any(word in query for word in [
        "tooth",
        "teeth",
        "dental"
    ]):

        specialist = "Dentist"



    elif any(word in query for word in [
        "stomach",
        "gastric",
        "digestion",
        "abdominal",
        "digestive",
        "digestive issues",
        "bowel",
        "constipation",
        "diarrhea",
        "acid reflux",
        "gerd"
    ]):

        specialist = "Gastroenterologist"



    state["specialist"] = specialist


    state["next_agent"] = "clinical"


    return state







# ==================================================
# Agent 3
# Clinical Care Agent
# ==================================================

def clinical_care_agent(state):


    query = state.get(
        "query",
        ""
    ).lower()



    # ==========================================
    # MRI / Insurance related request
    # ==========================================

    if (
        "mri" in query
        or
        "scan" in query
        or
        "insurance" in query
        or
        "coverage" in query
        or
        "claim" in query
    ):


        state["recommended_treatment"] = "MRI"


        state["next_agent"] = "insurance"


        return state




    # ==========================================
    # Doctor Appointment Booking
    # ==========================================


    specialist = state.get(
        "specialist",
        "General Physician"
    )



    appointment = book_doctor(
        specialist
    )



    print(
        "APPOINTMENT:",
        appointment
    )



    state["specialist"] = specialist


    state["appointment"] = appointment




    # ==========================================
    # Appointment Email Trigger
    # ==========================================


    trigger_n8n(

        "appointment_booking",

        {

        "patient_id":
        state.get(
            "patient_id",
            ""
        ),


        "patient_name":
        state.get(
            "patient_name",
            ""
        ),


        "patient_email":
        state.get(
            "patient_email",
            ""
        ),


        "patient_mobile":
        state.get(
            "patient_mobile",
            ""
        ),


        "age":
        state.get(
            "age",
            ""
        ),


        "gender":
        state.get(
            "gender",
            ""
        ),


        **appointment

        }

    )




    # ==========================================
    # Continue Workflow
    # ==========================================


    state["next_agent"] = "billing"



    return state




    # ==========================================
    # Treatment Detection
    # ==========================================


    if (

        "mri" in query

        or

        "scan" in query

        or

        "test" in query

        or

        "blood test" in query

    ):


        state["recommended_treatment"] = "MRI"



        # Move to insurance verification

        state["next_agent"] = "insurance"



    else:


        # Normal billing flow

        state["next_agent"] = "billing"




    return state


# ==================================================
# Agent 3
# Medical Knowledge Agent (RAG)
# ==================================================

def medical_knowledge_agent(state):


    query = state["query"]



    context = search_knowledge(
        query
    )



    prompt = f"""

You are a medical knowledge assistant.

Use only the provided context.

Do not diagnose.

Do not prescribe.

Context:

{context}


Question:

{query}

"""



    
    response = get_agent_llm().invoke(prompt)

    print("LLM RESPONSE:")
    print(response)



    state["response"] = response.content


    return state





# ==================================================
# Agent 4
# Pharmacy Agent
# ==================================================

def pharmacy_agent(state):


    medicine = "paracetamol"



    available = check_medicine(
        medicine
    )



    state["medicine"] = {


        "name": medicine,

        "available": available

    }



    trigger_n8n(

        "medicine_order",

        state["medicine"]

    )



    return state





# ==================================================
# Agent 5
# Insurance Agent
# ==================================================


def insurance_agent(state):


    query = state.get(
        "query",
        ""
    ).lower()



    # Detect treatment from user request

    treatment = state.get(
        "recommended_treatment"
    )


    if not treatment:


        if "mri" in query:

            treatment = "MRI"


        elif "scan" in query:

            treatment = "Scan"


        elif "test" in query:

            treatment = "Medical Test"


        else:

            treatment = "MRI"



    # Insurance coverage check

    coverage = check_insurance(
        treatment
    )



    state["insurance_status"] = {


        "treatment":
        treatment,


        "coverage":
        coverage

    }




    # Create claim

    claim = create_claim(

        state.get(
            "patient_id",
            "P001"
        ),

        treatment,

        1500

    )



    # attach email

    claim["patient_email"] = state.get(
        "patient_email",
        ""
    )



    state["claim"] = claim




    # n8n insurance workflow

    trigger_n8n(
    "insurance_claim",
    {
        **claim,

        "patient_email":
        state.get(
            "patient_email",
            ""
        ),

        "patient_name":
        state.get(
            "patient_name",
            ""
        ),

        "patient_id":
        state.get(
            "patient_id",
            ""
        )
    }
)



    state["recommended_treatment"] = treatment



    state["next_agent"] = "billing"



    return state



# ==================================================
# Agent 6
# Billing Agent
# ==================================================


def billing_agent(state):


    query = state.get(
        "query",
        ""
    ).lower()



    treatment = state.get(
        "recommended_treatment"
    )



    if not treatment:


        if "invoice" in query:

            treatment = "Treatment Invoice"


        elif "bill" in query:

            treatment = "Treatment Invoice"


        elif "payment" in query:

            treatment = "Treatment Invoice"


        else:

            treatment = "Doctor Visit"




    invoice = generate_invoice(


        state.get(
            "patient_id",
            "P001"
        ),


        treatment,


        1500

    )



    invoice["patient_email"] = state.get(
        "patient_email",
        ""
    )



    state["billing"] = invoice





    # ==============================================
    # Send invoice email ONLY when user asks invoice
    # ==============================================


    if (

        "invoice" in query

        or

        "bill" in query

        or

        "payment" in query

    ):


        trigger_n8n(

            "invoice_email",

            {

            **invoice,


            "patient_email":

            state.get(
                "patient_email",
                ""
            ),


            "patient_name":

            state.get(
                "patient_name",
                ""
            )

            }

        )



    return state


# ==================================================
# Agent 7
# Hospital Operations Agent
# ==================================================

def hospital_operations_agent(state):


    hospital_status = {


        "available_doctors": 25,

        "available_beds": 10,

        "emergency_queue": 3


    }



    state["hospital_operations"] = hospital_status



    return state


# ==================================================
# Guardrails Validation Agent
# ==================================================

def guardrails_agent(state):


    response = state.get(
        "response",
        ""
    )


    validated = validate_response(
        response
    )


    state["response"] = str(
        validated
    )


    return state
    





# ==================================================
# Agent 8
# Safety & Compliance Agent
# ==================================================

def safety_compliance_agent(state):


    response = state.get(
        "response",
        ""
    )



    state["response"] = f"""

{response}


IMPORTANT:

This AI assistant provides
health information support only.

Consult a licensed healthcare
professional for medical decisions.

Emergency symptoms require immediate
medical attention.

"""



    return state