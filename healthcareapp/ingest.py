from healthcareapp.rag import (
    ingest_medical,
    ingest_pharmacy,
    ingest_insurance
)



print("Starting ingestion...")


print("Loading medical documents")

ingest_medical()



print("Loading pharmacy documents")

ingest_pharmacy()



print("Loading insurance documents")

ingest_insurance()



print("All documents indexed successfully")

