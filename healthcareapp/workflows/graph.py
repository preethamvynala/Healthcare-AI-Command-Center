from langgraph.graph import StateGraph, END

from healthcareapp.state import HealthcareState
from healthcareapp.guardrails import validate_response


from healthcareapp.agents import (

    patient_care_coordinator_agent,
    specialist_router_agent,

    clinical_care_agent,

    medical_knowledge_agent,

    pharmacy_agent,

    insurance_agent,

    billing_agent,

    hospital_operations_agent,
    

    safety_compliance_agent

)



# Create graph

graph = StateGraph(
    HealthcareState
)



# =================================================
# Add Nodes (8 Agents)
# =================================================


graph.add_node(

    "patient",

    patient_care_coordinator_agent

)

graph.add_node(
    "specialist_router",
    specialist_router_agent
)



graph.add_node(

    "clinical",

    clinical_care_agent

)



graph.add_node(

    "medical_knowledge",

    medical_knowledge_agent

)



graph.add_node(

    "pharmacy",

    pharmacy_agent

)



graph.add_node(

    "insurance",

    insurance_agent

)



graph.add_node(

    "billing",

    billing_agent

)



graph.add_node(

    "operations",

    hospital_operations_agent

)

graph.add_node(
    "guardrails",
    validate_response
)



graph.add_node(

    "safety",

    safety_compliance_agent

)





# =================================================
# Entry Point
# =================================================


graph.set_entry_point(
    "patient"
)





# =================================================
# Router
# Patient Coordinator decides next agent
# =================================================


def router(state):

    return state["next_agent"]





graph.add_conditional_edges(

    "patient",

    router,

    {


        "clinical":
        "specialist_router",


        "pharmacy":
        "pharmacy",


        "insurance":
        "insurance",


        "billing":
        "billing",


        "operations":
        "operations",


        "medical_knowledge":
        "medical_knowledge"


    }

)

# =================================================
# Specialist Router -> Clinical
# =================================================


graph.add_edge(

    "specialist_router",

    "clinical"

)






# =================================================
# Agent Workflow Edges
# =================================================


# Clinical flow
graph.add_conditional_edges(

    "clinical",

    lambda state: state.get(
        "next_agent"
    ),


    {


    "insurance":
    "insurance",


    "billing":
    "billing"


    }

)




# Pharmacy flow

graph.add_edge(

    "pharmacy",

    "guardrails"

)



# Insurance flow

graph.add_edge(

    "insurance",

    "guardrails"

)



# Medical RAG flow

graph.add_edge(
    "medical_knowledge",
    "guardrails"
)


def guardrails_router(state):

    if state.get("next_agent") == "safety":
        return "safety"

    return "end"


graph.add_conditional_edges(

    "guardrails",

    guardrails_router,
    {
        "safety": "safety",
        "end": END
    }
)



# Billing flow

graph.add_edge(

    "billing",

    "guardrails"

)



# Hospital operations flow

graph.add_edge(

    "operations",

    "guardrails"

)





# =================================================
# Safety is final checkpoint
# =================================================


graph.add_edge(

    "safety",

    END

)





# Compile graph

healthcare_graph = graph.compile()