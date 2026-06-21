import os
import sys

from dotenv import load_dotenv


BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

sys.path.append(BASE_DIR)


load_dotenv(
    os.path.join(BASE_DIR, ".env")
)


from langchain_community.document_loaders import PyPDFLoader

from langchain_text_splitters import RecursiveCharacterTextSplitter


from database.chromadb.vector_store import (
    medical_vectorstore,
    pharmacy_vectorstore,
    insurance_vectorstore
)



# -----------------------------
# Lazy vector stores
# -----------------------------

_medical_db = None
_pharmacy_db = None
_insurance_db = None



def get_medical_db():

    global _medical_db

    if _medical_db is None:

        _medical_db = get_vector_store(
            "medical_collection"
        )

    return _medical_db




def get_pharmacy_db():

    global _pharmacy_db

    if _pharmacy_db is None:

        _pharmacy_db = get_vector_store(
            "pharmacy_collection"
        )

    return _pharmacy_db




def get_insurance_db():

    global _insurance_db

    if _insurance_db is None:

        _insurance_db = get_vector_store(
            "insurance_collection"
        )

    return _insurance_db




# -----------------------------
# PDF loading
# ONLY used locally
# -----------------------------


def load_pdf(path):

    loader = PyPDFLoader(path)

    return loader.load()




def split_documents(documents):

    splitter = RecursiveCharacterTextSplitter(

        chunk_size=1200,

        chunk_overlap=100
    )

    return splitter.split_documents(
        documents
    )




# -----------------------------
# INGEST
# DO NOT RUN ON RENDER
# -----------------------------


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


    db=get_medical_db()

    db.add_documents(docs)




def ingest_pharmacy():

    docs = split_documents(

        load_pdf(
            "data/pharmacy/drug_information.pdf"
        )
    )


    db=get_pharmacy_db()

    db.add_documents(docs)





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


    db=get_insurance_db()


    db.add_documents(docs)




# -----------------------------
# SEARCH
# Used by agents
# -----------------------------


def search_knowledge(
        query,
        domain="medical"
):


    if domain=="medical":

        db=get_medical_db()


    elif domain=="pharmacy":

        db=get_pharmacy_db()


    else:

        db=get_insurance_db()



    retriever=db.as_retriever(

        search_kwargs={
            "k":3
        }

    )


    results=retriever.invoke(query)


    return results