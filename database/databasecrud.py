from database.models import Patient



def create_patient(
    db,
    patient
):


    db.add(patient)

    db.commit()

    db.refresh(patient)


    return patient





def get_patient(
    db,
    patient_id
):


    return db.query(
        Patient
    ).filter(

        Patient.id==patient_id

    ).first()




def update_patient(
    db,
    patient_id,
    name
):


    patient=get_patient(
        db,
        patient_id
    )


    patient.name=name


    db.commit()


    return patient
