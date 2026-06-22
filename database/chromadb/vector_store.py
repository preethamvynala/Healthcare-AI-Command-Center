from langchain_chroma import Chroma

from database.chromadb.embeddings import get_embeddings

import os


BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)


CHROMA_PATH=os.path.join(
    BASE_DIR,
    "database",
    "chromadb",
    "collections"
)



def get_vector_store(
        collection_name
):


    embeddings=get_embeddings()



    vectorstore=Chroma(

        collection_name=collection_name,

        embedding_function=embeddings,

        persist_directory=CHROMA_PATH

    )


    return vectorstore






def medical_vectorstore():

    return get_vector_store(

        "medical_collection"

    )





def pharmacy_vectorstore():

    return get_vector_store(

        "pharmacy_collection"

    )





def insurance_vectorstore():

    return get_vector_store(

        "insurance_collection"

    )
