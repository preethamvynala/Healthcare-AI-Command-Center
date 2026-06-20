from langchain_community.vectorstores import Chroma

from langchain_google_genai import GoogleGenerativeAIEmbeddings



embeddings = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001"
)


memory_db = Chroma(

    persist_directory="patient_memory",

    embedding_function=embeddings

)



def save_memory(
        patient_id,
        text
):

    memory_db.add_texts(

        [
        text
        ],

        metadatas=[

        {
        "patient_id":patient_id
        }

        ]

    )



def get_memory(
        patient_id
):

    result=memory_db.similarity_search(

        patient_id,

        k=5

    )

    return result