from typing import TypedDict, Optional, Any



class HealthcareState(TypedDict):


    patient_id: str
    patient_name: Optional[str]

    patient_email: Optional[str]

    patient_mobile: Optional[str]

    age: Optional[int]

    gender: Optional[str]


    query: str


    department: Optional[str]


    specialist: Optional[str]


    appointment: dict
    recommended_treatment: str


    insurance_status: dict
    claim: dict


    medicine: Optional[Any]


    billing: dict


    hospital_operations: Optional[Any]


    response: Optional[str]


    next_agent: Optional[str]


    approval_required: Optional[bool]


    approved: Optional[bool]