-- Patients table

CREATE TABLE IF NOT EXISTS patients
(

    id SERIAL PRIMARY KEY,

    name VARCHAR(100),

    age INTEGER,

    gender VARCHAR(20),

    phone VARCHAR(20),

    blood_group VARCHAR(10),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);



-- Doctors

CREATE TABLE IF NOT EXISTS doctors
(

    id SERIAL PRIMARY KEY,

    name VARCHAR(100),

    speciality VARCHAR(100),

    availability VARCHAR(100)

);




-- Appointments

CREATE TABLE IF NOT EXISTS appointments
(

    id SERIAL PRIMARY KEY,

    patient_id INTEGER,

    doctor_id INTEGER,

    appointment_date TIMESTAMP,

    status VARCHAR(50),


    FOREIGN KEY(patient_id)
    REFERENCES patients(id),


    FOREIGN KEY(doctor_id)
    REFERENCES doctors(id)

);





-- Insurance Claims


CREATE TABLE IF NOT EXISTS insurance_claims
(

    id SERIAL PRIMARY KEY,

    patient_id INTEGER,

    provider VARCHAR(100),

    amount FLOAT,

    status VARCHAR(50),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);





-- Billing


CREATE TABLE IF NOT EXISTS invoices
(

    id SERIAL PRIMARY KEY,

    patient_id INTEGER,

    amount FLOAT,

    payment_status VARCHAR(50)

);





-- Agent Memory


CREATE TABLE IF NOT EXISTS agent_memory
(

id SERIAL PRIMARY KEY,

patient_id INTEGER,

conversation TEXT,

created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);
