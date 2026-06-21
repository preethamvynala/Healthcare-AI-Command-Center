def get_graph():

    from healthcareapp.workflows.graph import healthcare_graph

    return healthcare_graph




def run_agent(
        question,
        patient_id,
        patient_name,
        patient_email,
        patient_mobile,
        age,
        gender
):


    initial_state = {


        "patient_id":
        patient_id,


        "patient_name":
        patient_name,


        "patient_email":
        patient_email,


        "patient_mobile":
        patient_mobile,


        "age":
        age,


        "gender":
        gender,



        "query":
        question,



        "department":
        None,


        "specialist":
        None,


        "appointment":
        None,


        "insurance_status":
        None,


        "medicine":
        None,


        "billing":
        None,


        "hospital_operations":
        None,
        "invoice":
        None,
        "claim":
        None,
        "recommended_treatment":
        None,



        "response":
        "",


        "next_agent":
        None,


        "approval_required":
        False,


        "approved":
        False

    }



    graph = get_graph()

    result = graph.invoke(
        initial_state
)



    return result






if __name__ == "__main__":


    response = run_agent(

        question=
        "What are symptoms of heart disease?",
        patient_id="P001",


        patient_name=
        "Demo Patient",


        patient_email=
        "patient@gmail.com",


        patient_mobile=
        "9999999999",


        age=
        30,


        gender=
        "Male"

    )


    print(response)