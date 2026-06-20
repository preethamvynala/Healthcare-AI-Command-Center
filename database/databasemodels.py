from sqlalchemy import Column,Integer,String,Float,Text

from database.db import engine

from sqlalchemy.orm import declarative_base



Base=declarative_base()



class Patient(Base):

    __tablename__="patients"


    id=Column(
        Integer,
        primary_key=True
    )


    name=Column(
        String
    )


    age=Column(
        Integer
    )


    gender=Column(
        String
    )


    phone=Column(
        String
    )





class Doctor(Base):

    __tablename__="doctor"


    id=Column(
        Integer,
        primary_key=True
    )


    name=Column(String)


    speciality=Column(String)



Base.metadata.create_all(
    engine
)
