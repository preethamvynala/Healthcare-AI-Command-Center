INSERT INTO patients
(
name,
age,
gender,
phone,
blood_group
)

VALUES

(
'John Smith',
45,
'Male',
'9999999999',
'O+'
);



INSERT INTO doctors
(
name,
speciality,
availability
)

VALUES

(
'Dr Ahmed',
'Cardiology',
'Monday 10 AM'
);



INSERT INTO doctors
(
name,
speciality,
availability
)

VALUES

(
'Dr Sara',
'Orthopedics',
'Tuesday 2 PM'
);



INSERT INTO insurance_claims
(
patient_id,
provider,
amount,
status
)

VALUES

(
1,
'ABC Insurance',
5000,
'Pending'
);
