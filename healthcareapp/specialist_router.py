from typing import Dict


def specialist_router_agent(state) -> Dict:


    query = state["query"].lower()


    specialist = "General Physician"



    # Cardiology

    if any(word in query for word in [

        "chest pain",
        "heart",
        "cardiac",
        "palpitation",
        "blood pressure",
        "heartbeat"

    ]):

        specialist = "Cardiologist"



    # Dermatology

    elif any(word in query for word in [

        "skin",
        "rash",
        "itching",
        "acne",
        "dermatitis",
        "pimples",
        "eczema"

    ]):

        specialist = "Dermatologist"



    # Neurology

    elif any(word in query for word in [

        "brain",
        "headache",
        "seizure",
        "memory",
        "migraine",
        "dizziness"

    ]):

        specialist = "Neurologist"



    # Gastroenterology  

    elif any(word in query for word in [

        "stomach",
        "digestive",
        "digestive issues",
        "digestion",
        "gastric",
        "acid reflux",
        "gerd",
        "constipation",
        "diarrhea",
        "bowel",
        "abdominal pain"

    ]):

        specialist = "Gastroenterologist"



    # Orthopedic

    elif any(word in query for word in [

        "bone",
        "fracture",
        "joint",
        "back pain",
        "muscle pain"

    ]):

        specialist = "Orthopedist"



    # ENT

    elif any(word in query for word in [

        "ear",
        "nose",
        "throat",
        "sinus"

    ]):

        specialist = "ENT Specialist"



    # Dental

    elif any(word in query for word in [

        "tooth",
        "teeth",
        "dental",
        "gum"

    ]):

        specialist = "Dentist"



    return {


        "specialist": specialist,

        "next_agent": "clinical"

    }