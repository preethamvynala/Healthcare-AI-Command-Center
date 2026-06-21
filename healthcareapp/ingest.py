"""
Manual ingestion script.

Do not run automatically on cloud deployment.

Run locally only:

python -m healthcareapp.ingest
"""


from healthcareapp.rag import (
    ingest_medical,
    ingest_pharmacy,
    ingest_insurance
)


if __name__=="__main__":

    print("Starting ingestion")


    ingest_medical()

    ingest_pharmacy()

    ingest_insurance()


    print("Completed")