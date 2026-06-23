import requests
import os

from dotenv import load_dotenv

load_dotenv()



# =====================================================
# n8n Automation Tool
# =====================================================


import os
import requests



def trigger_n8n(event, data):


    urls = {


        "appointment_booking":
        os.getenv(
            "N8N_WEBHOOK_URL"
        ),


        "insurance_claim":
        os.getenv(
            "N8N_INSURANCE_WEBHOOK_URL"
        ),


        "invoice_email":
        os.getenv(
            "N8N_INVOICE_WEBHOOK_URL"
        )

    }



    url = urls.get(event)



    if not url:

        print(
            f"N8N webhook missing for {event}"
        )

        return {

            "status":"missing webhook"

        }





    payload = {


        "event": event,


        "data": data


    }




    try:


        response = requests.post(

            url,

            json=payload,

            timeout=90

        )



        print(
            "N8N RESPONSE:",
            response.status_code,
            response.text
        )



        return {


            "status":"sent",


            "code":
            response.status_code,


            "response":
            response.text

        }




    except Exception as e:



        print(
            "N8N ERROR:",
            e
        )



        return {


            "status":"n8n_failed",


            "error":str(e)

        }



# =====================================================
# Doctor Appointment Tool
# =====================================================

def book_doctor(
        speciality
):


    doctors = {

        "Cardiologist": {
            "doctor": "Dr. Rajesh Sharma",
            "day": "Monday",
            "time": "10:00 AM"
        },

        "Dermatologist": {
            "doctor": "Dr. Priya Reddy",
            "day": "Tuesday",
            "time": "11:00 AM"
        },

        "Neurologist": {
            "doctor": "Dr. Anil Rao",
            "day": "Wednesday",
            "time": "02:00 PM"
        },

        "Orthopedist": {
            "doctor": "Dr. Arjun Patel",
            "day": "Thursday",
            "time": "03:00 PM"
        },

        "ENT Specialist": {
            "doctor": "Dr. Kavya Menon",
            "day": "Friday",
            "time": "09:00 AM"
        },

        "Dentist": {
            "doctor": "Dr. Sneha Kapoor",
            "day": "Saturday",
            "time": "12:00 PM"
        },

        "Gastroenterologist": {
            "doctor": "Dr. Vivek Nair",
            "day": "Monday",
            "time": "04:00 PM"
        },

        "General Physician": {
            "doctor": "Dr. Amit Kumar",
            "day": "Monday",
            "time": "10:00 AM"
        }

    }


    selected = doctors.get(
        speciality,
        doctors["General Physician"]
    )


    return {

        "doctor": selected["doctor"],

        "speciality": speciality,

        "day": selected["day"],

        "time": selected["time"],

        "status": "confirmed"

    }





# =====================================================
# Pharmacy Tool
# =====================================================

def check_medicine(
        medicine
):


    # Demo inventory
    medicines = {

        "paracetamol": True,

        "ibuprofen": True,

        "amoxicillin": True,

        "vitamin d": True

    }



    available = medicines.get(

        medicine.lower(),

        False

    )


    return {

        "medicine": medicine,

        "available": available

    }





# =====================================================
# Insurance Tool
# =====================================================

def check_insurance(
        treatment
):


    covered_services = [

        "MRI",

        "doctor consultation",

        "blood test"

    ]


    if treatment in covered_services:

        status = "Covered"

    else:

        status = "Not Covered"



    return {

        "treatment": treatment,

        "status": status

    }


def create_claim(
    patient_id,
    treatment,
    amount
):

    claim = {


        "claim_id":
        "CLM-" + patient_id,


        "treatment":
        treatment,


        "amount":
        amount,


        "status":
        "submitted"



    }


    return claim


def generate_invoice(
    patient_id,
    treatment,
    amount
):


    patient_id = patient_id or "P001"
    invoice={


        "invoice_id":
        "INV-" + patient_id,


        "patient_id":
        patient_id,


        "service":
        treatment,


        "amount":
        amount,


        "currency":
        "AED",


        "status":
        "generated"

    }


    return invoice