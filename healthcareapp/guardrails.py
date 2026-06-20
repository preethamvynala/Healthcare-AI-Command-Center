from typing import Dict


def validate_response(state: Dict):


    query = state.get(
        "query",
        ""
    ).lower()


    response = state.get(
        "response",
        ""
    )


    emergency_keywords = [

        "chest pain",
        "difficulty breathing",
        "unconscious",
        "severe bleeding",
        "stroke"

    ]


    for word in emergency_keywords:

        if word in query:


            state["response"] = (

                "Chest pain or similar symptoms "
                "may require urgent medical attention.\n\n"

                "Please contact emergency services "
                "or visit the nearest emergency department.\n\n"

                "This AI assistant provides "
                "health information support only."

            )


            # IMPORTANT FIX
            state["next_agent"] = "safety"


            # remove old appointment data
            state["appointment"] = None


            return state



    blocked_patterns = [

        "you have",
        "diagnosed with",
        "confirmed disease",
        "take this medicine",
        "you should take",
        "prescription"

    ]



    for pattern in blocked_patterns:


        if pattern in response.lower():


            state["response"] = (

                "I can provide general healthcare information, "
                "but I cannot diagnose conditions or prescribe "
                "medications.\n\n"

                "Please consult a licensed healthcare professional."

            )


            break



    return state