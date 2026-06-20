import os


from dotenv import load_dotenv


load_dotenv()
from langchain_community.document_loaders import PyPDFLoader

from langchain_text_splitters import RecursiveCharacterTextSplitter

from database.chromadb.vector_store import (
    medical_vectorstore,
    pharmacy_vectorstore,
    insurance_vectorstore
)







def load_pdf(path):


    loader=PyPDFLoader(path)


    documents=loader.load()


    return documents





def split_documents(documents):


    splitter=RecursiveCharacterTextSplitter(

        chunk_size=1200,

        chunk_overlap=100

    )


    chunks=splitter.split_documents(
        documents
    )


    return chunks





def ingest_medical():



    files=[

    "data/medical/guidelines.pdf",

    "data/medical/patient_guides.pdf",

    "data/medical/clinical_protocols.pdf"

    ]



    docs=[]


    for file in files:

        docs.extend(

            split_documents(
                load_pdf(file)
            )

        )



    db=medical_vectorstore()


    db.add_documents(
        docs
    )





def ingest_pharmacy():


    docs=split_documents(

        load_pdf(
        "data/pharmacy/drug_information.pdf"
        )

    )


    db=pharmacy_vectorstore()


    db.add_documents(
        docs
    )







def ingest_insurance():


    files=[

    "data/insurance/policies.pdf",

    "data/insurance/claims.pdf"

    ]



    docs=[]


    for file in files:

        docs.extend(

        split_documents(
            load_pdf(file)
        )

        )



    db=insurance_vectorstore()


    db.add_documents(
        docs
    )







def search_knowledge(
        query,
        domain="medical"
):



    if domain=="medical":

        db=medical_vectorstore()


    elif domain=="pharmacy":

        db=pharmacy_vectorstore()


    else:

        db=insurance_vectorstore()



    retriever=db.as_retriever(

        search_kwargs={
            "k":3
        }

    )


    results=retriever.invoke(
        query
    )


    return results
